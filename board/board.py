#!/usr/bin/env python3
"""board.py — deterministic operations for a git-file-backed ticket board.

One helper, three consumers: board-lead (creates tickets), board-work (claims
and completes them), board-watch (monitors the fleet). It owns the mechanical,
easy-to-get-wrong parts — atomic claims, dependency-aware selection, status
transitions, the rendered index, checkpoints, and the liveness summary — so the
agents can spend their judgment on the actual work.

State is plain files under <repo>/board/, all git-tracked:

    board/
      board.config.json     # board settings (stale threshold, etc.)
      tickets/T-001.md       # one markdown file per ticket, YAML-ish frontmatter
      BOARD.md               # rendered kanban index (generated; do not hand-edit)
      CHECKPOINT.md          # last checkpoint snapshot (generated)
      .locks/T-001.lock      # exclusive-create claim guard (gitignored)

Design choices worth knowing:
  * The claim guard is an atomic exclusive file create (open 'x'), robust across
    processes on one machine. For cross-machine work over a git remote, claims
    are also a committed status flip — push rejection is the tiebreak (see
    AGENTS.md). Two guards, because two topologies.
  * Frontmatter is parsed with a tiny purpose-built reader, not PyYAML — zero
    dependencies so this runs in any harness's environment.
  * This file is committed INTO the board (board/board.py) by `init`, so it
    travels with the repo. Every harness runs the same code on the same state.

Usage:
    python board/board.py <command> [args]

Commands (see --help on each is not implemented; read this header):
    init [--repo PATH]                 scaffold board/ in a git repo
    add --title T [--depends A,B] [--priority N] [--harness H] [--body FILE]
    list [--status S] [--json]         show tickets
    show T-NNN                         print one ticket
    next [--harness H] [--json]        highest-priority unblocked todo ticket
    claim T-NNN --owner ID             atomic claim (todo -> in_progress)
    set-status T-NNN STATUS [--owner ID] [--pr URL] [--note TEXT]
    heartbeat T-NNN --owner ID         record liveness for the watcher
    render                             regenerate BOARD.md
    checkpoint [--tag NAME] [--message M]   render + commit board snapshot
    summary [--json] [--stale-min N]   fleet health for board-watch
    stale [--stale-min N] [--json]     in_progress tickets with no recent life
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STATUSES = ["todo", "in_progress", "in_review", "done", "blocked"]
TERMINAL = {"done"}


# ---------------------------------------------------------------------------
# Board location
# ---------------------------------------------------------------------------
def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(args, cwd, check=True):
    r = subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True
    )
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{r.stderr.strip()}")
    return r


def find_board(start: Path | None = None) -> Path:
    """Locate the board/ directory. Prefer this file's own parent (the copy
    committed into the repo); otherwise walk up from cwd."""
    here = Path(__file__).resolve().parent
    if (here / "board.config.json").exists():
        return here
    cur = (start or Path.cwd()).resolve()
    for d in [cur, *cur.parents]:
        cand = d / "board"
        if (cand / "board.config.json").exists():
            return cand
    sys.exit(
        "error: no board found. Run `board.py init` in a git repo first, "
        "or cd into a repo that has a board/ directory."
    )


def repo_root(board_dir: Path) -> Path:
    r = git(["rev-parse", "--show-toplevel"], board_dir, check=False)
    if r.returncode == 0 and r.stdout.strip():
        return Path(r.stdout.strip())
    return board_dir.parent


# ---------------------------------------------------------------------------
# Frontmatter (tiny, dependency-free)
# ---------------------------------------------------------------------------
def parse_frontmatter(text: str):
    """Return (meta: dict, body: str). Supports `key: value`, `key: [a, b]`,
    `key: null`, and quoted strings. Deliberately small — the format is ours."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    head = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")
    meta = {}
    for line in head.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        meta[key] = _coerce(val)
    return meta, body


def _coerce(val: str):
    if val == "" or val.lower() in ("null", "none", "~"):
        return None
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
    if (val.startswith('"') and val.endswith('"')) or (
        val.startswith("'") and val.endswith("'")
    ):
        return val[1:-1]
    if val.isdigit():
        return int(val)
    return val


def dump_frontmatter(meta: dict, body: str) -> str:
    order = [
        "id", "title", "status", "owner", "priority", "depends_on",
        "branch", "worktree", "harness_hint", "pr", "created",
        "claimed_at", "heartbeat", "updated", "note",
    ]
    keys = [k for k in order if k in meta] + [k for k in meta if k not in order]
    lines = ["---"]
    for k in keys:
        lines.append(f"{k}: {_fmt(meta[k])}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.rstrip() + "\n"


def _fmt(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return "[" + ", ".join(str(x) for x in v) + "]"
    return str(v)


# ---------------------------------------------------------------------------
# Ticket access
# ---------------------------------------------------------------------------
def tickets_dir(board: Path) -> Path:
    return board / "tickets"


def read_ticket(path: Path):
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    meta.setdefault("id", path.stem)
    meta["_path"] = str(path)
    meta["_body"] = body
    return meta


def all_tickets(board: Path):
    out = []
    tdir = tickets_dir(board)
    if not tdir.exists():
        return out
    for p in sorted(tdir.glob("T-*.md")):
        out.append(read_ticket(p))
    return out


def get_ticket(board: Path, tid: str):
    p = tickets_dir(board) / f"{tid}.md"
    if not p.exists():
        sys.exit(f"error: no such ticket {tid}")
    return read_ticket(p)


def write_ticket(meta: dict):
    path = Path(meta.pop("_path"))
    body = meta.pop("_body", "")
    path.write_text(dump_frontmatter(meta, body), encoding="utf-8")


def next_id(board: Path) -> str:
    n = 0
    for t in all_tickets(board):
        try:
            n = max(n, int(str(t["id"]).split("-")[1]))
        except (IndexError, ValueError):
            pass
    return f"T-{n + 1:03d}"


def deps_done(board: Path, meta: dict, by_id: dict) -> bool:
    for dep in meta.get("depends_on") or []:
        d = by_id.get(dep)
        if not d or d.get("status") not in TERMINAL:
            return False
    return True


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
def cmd_init(args):
    repo = Path(args.repo or Path.cwd()).resolve()
    if git(["rev-parse", "--is-inside-work-tree"], repo, check=False).returncode != 0:
        sys.exit(
            f"error: {repo} is not a git repository. `git init` first "
            "(worktrees and per-ticket branches require git)."
        )
    board = repo / "board"
    (board / "tickets").mkdir(parents=True, exist_ok=True)
    (board / ".locks").mkdir(exist_ok=True)
    cfg = board / "board.config.json"
    if not cfg.exists():
        cfg.write_text(json.dumps({
            "created": now_iso(),
            "stale_minutes": 30,
            "worktree_root": "../worktrees",
            "pr_mode": "gh",  # gh | record (local PR-record files)
        }, indent=2), encoding="utf-8")
    # Copy this helper into the board so every harness runs identical code.
    dst = board / "board.py"
    if Path(__file__).resolve() != dst.resolve():
        dst.write_text(Path(__file__).read_text(encoding="utf-8"), encoding="utf-8")
    gi = board / ".gitignore"
    gi.write_text(".locks/\n", encoding="utf-8")
    render(board)
    print(f"Initialized board at {board}")
    print("Next: create tickets with `python board/board.py add --title ...`")
    print("Then commit: git add board && git commit -m 'chore: init ticket board'")


def cmd_add(args):
    board = find_board()
    tid = next_id(board)
    body = ""
    if args.body:
        body = Path(args.body).read_text(encoding="utf-8")
    else:
        body = TICKET_BODY_STUB
    meta = {
        "id": tid,
        "title": args.title,
        "status": "todo",
        "owner": None,
        "priority": args.priority,
        "depends_on": args.depends.split(",") if args.depends else [],
        "branch": f"ticket/{tid}",
        "worktree": None,
        "harness_hint": args.harness,
        "pr": None,
        "created": now_iso(),
        "_path": str(tickets_dir(board) / f"{tid}.md"),
        "_body": body,
    }
    write_ticket(meta)
    render(board)
    print(tid)
    print(str(tickets_dir(board) / f"{tid}.md"))


def cmd_list(args):
    board = find_board()
    ts = all_tickets(board)
    if args.status:
        ts = [t for t in ts if t.get("status") == args.status]
    if args.json:
        print(json.dumps([_public(t) for t in ts], indent=2))
        return
    if not ts:
        print("(no tickets)")
        return
    for t in ts:
        dep = ",".join(t.get("depends_on") or []) or "-"
        owner = t.get("owner") or "-"
        print(f"{t['id']:>7}  {t.get('status',''):<12} p{t.get('priority','?')} "
              f"owner={owner:<12} deps={dep}  {t.get('title','')}")


def cmd_show(args):
    board = find_board()
    t = get_ticket(board, args.id)
    print(Path(t["_path"]).read_text(encoding="utf-8"))


def cmd_next(args):
    board = find_board()
    ts = all_tickets(board)
    by_id = {t["id"]: t for t in ts}
    cands = [
        t for t in ts
        if t.get("status") == "todo"
        and deps_done(board, t, by_id)
        and (not args.harness
             or t.get("harness_hint") in (None, "any", args.harness))
    ]
    cands.sort(key=lambda t: (t.get("priority") or 99, str(t["id"])))
    if not cands:
        print("{}" if args.json else "none")
        return
    pick = cands[0]
    if args.json:
        print(json.dumps(_public(pick), indent=2))
    else:
        print(pick["id"])


def cmd_claim(args):
    board = find_board()
    t = get_ticket(board, args.id)
    if t.get("status") != "todo":
        sys.exit(f"conflict: {args.id} is '{t.get('status')}', not claimable "
                 f"(owner={t.get('owner')})")
    lock = board / ".locks" / f"{args.id}.lock"
    lock.parent.mkdir(exist_ok=True)
    try:
        # Atomic guard: exclusive create fails if another worker beat us here.
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, f"{args.owner} {now_iso()}\n".encode())
        os.close(fd)
    except FileExistsError:
        sys.exit(f"conflict: {args.id} is being claimed by another worker")
    t["status"] = "in_progress"
    t["owner"] = args.owner
    t["claimed_at"] = now_iso()
    t["heartbeat"] = now_iso()
    t["updated"] = now_iso()
    write_ticket(t)
    render(board)
    print(f"claimed {args.id} for {args.owner}")


def cmd_set_status(args):
    board = find_board()
    t = get_ticket(board, args.id)
    if args.status not in STATUSES:
        sys.exit(f"error: status must be one of {STATUSES}")
    t["status"] = args.status
    if args.owner:
        t["owner"] = args.owner
    if args.pr:
        t["pr"] = args.pr
    if args.note:
        t["note"] = args.note
    t["updated"] = now_iso()
    # Release the claim lock once the ticket leaves active work.
    if args.status in ("done", "blocked", "todo"):
        lock = board / ".locks" / f"{args.id}.lock"
        if lock.exists():
            lock.unlink()
    write_ticket(t)
    render(board)
    print(f"{args.id} -> {args.status}")


def cmd_heartbeat(args):
    board = find_board()
    t = get_ticket(board, args.id)
    t["heartbeat"] = now_iso()
    if args.owner:
        t["owner"] = args.owner
    write_ticket(t)
    print(f"heartbeat {args.id} @ {t['heartbeat']}")


def cmd_render(args):
    board = find_board()
    render(board)
    print(f"rendered {board / 'BOARD.md'}")


def cmd_checkpoint(args):
    board = find_board()
    root = repo_root(board)
    render(board)
    s = _summary(board)
    stamp = now_iso()
    lines = [
        f"# Board checkpoint — {stamp}", "",
        f"- todo: {s['counts'].get('todo',0)}",
        f"- in_progress: {s['counts'].get('in_progress',0)}",
        f"- in_review: {s['counts'].get('in_review',0)}",
        f"- done: {s['counts'].get('done',0)}",
        f"- blocked: {s['counts'].get('blocked',0)}",
        f"- stale (no heartbeat > {s['stale_minutes']}m): "
        f"{', '.join(s['stale']) or 'none'}", "",
        "Resume: `python board/board.py summary` then re-dispatch stale/blocked "
        "tickets. Worktrees for in_progress tickets survive in the worktree root.",
    ]
    (board / "CHECKPOINT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    git(["add", "board"], root)
    msg = args.message or f"checkpoint: board @ {stamp}"
    r = git(["commit", "-m", msg], root, check=False)
    if r.returncode != 0 and "nothing to commit" in (r.stdout + r.stderr):
        print("checkpoint: no changes to commit")
    else:
        print(f"checkpoint committed: {msg}")
    if args.tag:
        git(["tag", "-f", args.tag], root, check=False)
        print(f"tagged {args.tag}")


def cmd_summary(args):
    board = find_board()
    s = _summary(board, args.stale_min)
    if args.json:
        print(json.dumps(s, indent=2))
        return
    c = s["counts"]
    total = sum(c.values())
    done = c.get("done", 0)
    print(f"Board: {done}/{total} done  |  " + "  ".join(
        f"{k}={c.get(k,0)}" for k in STATUSES))
    if s["ready"]:
        print(f"ready to dispatch: {', '.join(s['ready'])}")
    if s["stale"]:
        print(f"STALE (no heartbeat > {s['stale_minutes']}m): {', '.join(s['stale'])}")
    if s["blocked"]:
        print(f"blocked: {', '.join(s['blocked'])}")


def cmd_stale(args):
    board = find_board()
    s = _summary(board, args.stale_min)
    if args.json:
        print(json.dumps(s["stale"], indent=2))
    else:
        print("\n".join(s["stale"]) or "none")


def _age_minutes(iso: str | None):
    if not iso:
        return None
    try:
        t = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    return (datetime.now(timezone.utc) - t).total_seconds() / 60.0


def _summary(board: Path, stale_min=None):
    cfg = json.loads((board / "board.config.json").read_text(encoding="utf-8"))
    stale_min = stale_min or cfg.get("stale_minutes", 30)
    ts = all_tickets(board)
    by_id = {t["id"]: t for t in ts}
    counts = {s: 0 for s in STATUSES}
    stale, blocked, ready = [], [], []
    for t in ts:
        st = t.get("status", "todo")
        counts[st] = counts.get(st, 0) + 1
        if st == "blocked":
            blocked.append(t["id"])
        if st == "in_progress":
            age = _age_minutes(t.get("heartbeat"))
            if age is None or age > stale_min:
                stale.append(t["id"])
        if st == "todo" and deps_done(board, t, by_id):
            ready.append(t["id"])
    return {
        "counts": counts,
        "stale": stale,
        "stale_minutes": stale_min,
        "blocked": blocked,
        "ready": sorted(ready, key=lambda i: (by_id[i].get("priority") or 99, i)),
    }


def _public(t: dict):
    return {k: v for k, v in t.items() if not k.startswith("_")}


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
def render(board: Path):
    ts = all_tickets(board)
    by_status = {s: [] for s in STATUSES}
    for t in ts:
        by_status.setdefault(t.get("status", "todo"), []).append(t)
    lines = ["# Board", "",
             "<!-- generated by board.py — do not hand-edit; edit tickets/ -->", ""]
    total = len(ts)
    done = len(by_status.get("done", []))
    lines.append(f"**{done}/{total} done**  ·  "
                 + "  ·  ".join(f"{s}: {len(by_status.get(s, []))}" for s in STATUSES))
    lines.append("")
    for s in STATUSES:
        group = by_status.get(s, [])
        lines.append(f"## {s} ({len(group)})")
        if not group:
            lines.append("")
            continue
        lines.append("| id | pri | title | owner | deps | pr |")
        lines.append("|----|----|-------|-------|------|----|")
        for t in sorted(group, key=lambda x: (x.get("priority") or 99, str(x["id"]))):
            dep = ", ".join(t.get("depends_on") or []) or "—"
            lines.append(
                f"| {t['id']} | {t.get('priority','?')} | {t.get('title','')} "
                f"| {t.get('owner') or '—'} | {dep} | {t.get('pr') or '—'} |")
        lines.append("")
    (board / "BOARD.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


TICKET_BODY_STUB = """## Goal
<One paragraph: what "done" looks like, in outcome terms.>

## Context
<Pointers the worker needs: files, prior art, constraints, gotchas.>

## Acceptance criteria
- [ ] <observable behavior>
- [ ] Tests pass: <exact command>
- [ ] <lint/typecheck command if any>

## Notes for the worker
<Anything harness-specific or sequencing-sensitive.>
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(prog="board.py", add_help=True)
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init"); sp.add_argument("--repo"); sp.set_defaults(fn=cmd_init)

    sp = sub.add_parser("add")
    sp.add_argument("--title", required=True)
    sp.add_argument("--depends", default="")
    sp.add_argument("--priority", type=int, default=3)
    sp.add_argument("--harness", default="any")
    sp.add_argument("--body", help="path to a markdown file for the ticket body")
    sp.set_defaults(fn=cmd_add)

    sp = sub.add_parser("list")
    sp.add_argument("--status"); sp.add_argument("--json", action="store_true")
    sp.set_defaults(fn=cmd_list)

    sp = sub.add_parser("show"); sp.add_argument("id"); sp.set_defaults(fn=cmd_show)

    sp = sub.add_parser("next")
    sp.add_argument("--harness"); sp.add_argument("--json", action="store_true")
    sp.set_defaults(fn=cmd_next)

    sp = sub.add_parser("claim")
    sp.add_argument("id"); sp.add_argument("--owner", required=True)
    sp.set_defaults(fn=cmd_claim)

    sp = sub.add_parser("set-status")
    sp.add_argument("id"); sp.add_argument("status")
    sp.add_argument("--owner"); sp.add_argument("--pr"); sp.add_argument("--note")
    sp.set_defaults(fn=cmd_set_status)

    sp = sub.add_parser("heartbeat")
    sp.add_argument("id"); sp.add_argument("--owner"); sp.set_defaults(fn=cmd_heartbeat)

    sp = sub.add_parser("render"); sp.set_defaults(fn=cmd_render)

    sp = sub.add_parser("checkpoint")
    sp.add_argument("--tag"); sp.add_argument("--message")
    sp.set_defaults(fn=cmd_checkpoint)

    sp = sub.add_parser("summary")
    sp.add_argument("--json", action="store_true")
    sp.add_argument("--stale-min", type=int, dest="stale_min")
    sp.set_defaults(fn=cmd_summary)

    sp = sub.add_parser("stale")
    sp.add_argument("--json", action="store_true")
    sp.add_argument("--stale-min", type=int, dest="stale_min")
    sp.set_defaults(fn=cmd_stale)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
