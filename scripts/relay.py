#!/usr/bin/env python3
"""relay.py -- cross-harness context relay buffer (spiral mode).

Two or three agents in different harnesses work one repo on staggered context
lifecycles. Each keeps its OWN belief cell; the buffer makes divergence between
them visible instead of letting the last writer silently overwrite the rest.

  beliefs/<agent>.md   per-agent belief (the cell)  -- overwritten, size-capped
  journal.jsonl        decisions / dead ends        -- append-only, grep target
  divergence.jsonl     who disagreed, who was right -- the measurement payoff
  profiles/<h>.md      per-harness capability sheet -- the impedance match

The repo is the anchor. Agents reconcile against git and verify commands, never
against each other's beliefs alone: two agents agreeing is not evidence when both
derived from the same lossy source.

ASCII output only (the origin corpus's cp1252 console crash is a documented
incident). Stdlib only -- runs under whatever python a harness has on PATH.

Usage:
  relay.py init                                  scaffold workflow/relay/
  relay.py bootstrap <agent> --harness <h>       create a belief cell
  relay.py stamp <agent> [--context 0.42]        refresh meta (head/time/context)
  relay.py check <agent> [--json]                validation gate (exit 1 on fail)
  relay.py sync [--json]                         per-dimension SYNC/GAP/CONFLICT
  relay.py roles [--json]                        explorer/judge by remaining context
  relay.py note <agent> --kind <k> --text <t>    append to journal.jsonl
  relay.py resolve --dim <d> --winner <w>        append to divergence.jsonl
  relay.py status [--json]                       one-glance overview
  relay.py report [--json]                       is the spiral earning its cost?
  relay.py dispatch <agent>                      paste-able cross-harness boot block
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Dimensions of a belief cell. SINGULAR: any difference is a conflict (there is one
# truth). LIST: one side being a subset of the other is a GAP, not a conflict --
# the behind agent just needs to catch up.
SINGULAR = ["Objective", "State", "Next action"]
LIST = ["Dead ends", "Open questions", "Binding rules", "Requires"]
# Dimensions whose content is a token list, not prose lines. Compared token-wise,
# so "git python" vs "git python mcp:x" reads as a GAP and not a CONFLICT.
TOKEN_DIMS = {"Requires"}
DIMENSIONS = SINGULAR + LIST
REQUIRED = SINGULAR + ["Dead ends", "Open questions"]

LINE_CAP = 150
STALE_AFTER_MIN = 120
META_RE = re.compile(r"<!--\s*relay:meta\s*(.*?)-->", re.S)
PROFILE_RE = re.compile(r"<!--\s*relay:profile\s*(.*?)-->", re.S)

CELL_TEMPLATE = """<!-- relay:meta
agent: {agent}
harness: {harness}
updated: {updated}
head: {head}
context: 0.0
-->
# Belief -- {agent}

Your own view of the work. Overwrite it; do not append history. Anything derivable
from the repo belongs in the repo, not here. Keep it under {cap} lines.

## Objective
<what we are trying to achieve, in one or two lines>

## State
<where things actually are right now: branch, dirty files, what is mid-change>

## Next action
<the single next step, as a literal command or edit>

## Dead ends
<tried and failed, with why -- this is the only content that dies with you>
none

## Open questions
<unresolved, blocking or not>
none

## Binding rules
<the few house rules that constrain the NEXT action -- not the whole contract>
none

## Requires
<capabilities the next action needs: git, python, mcp:name, tool:name>
git

## Anchor
verify: <one command, seconds to run, that proves State is true>
"""

PROFILES = {
    "claude-code": "claude-code\nbash,powershell\ngit,python,rg,skill:phased,skill:handoff,mcp:local-memory",
    "codex": "codex\nbash\ngit,python",
}

README = """# relay -- cross-harness context relay buffer

Harness-neutral. Any agent that can read files and run git can use this. Nothing
here requires a slash command, a skill, or an MCP server.

## What this is

Two or three agents in different harnesses (Claude Code, Codex, ...) work the same
repo on staggered context lifecycles. Rather than one handing off to the next, they
orbit: each keeps its own belief cell, they compare cheap digests, and they
reconcile only where they disagree.

## The rules that make it work

1. ANCHOR TO THE REPO, NOT TO EACH OTHER. Every cycle, re-derive from git and from
   the verify command before comparing beliefs. Two agents agreeing is not evidence
   if both inherited the same wrong summary.
2. ROLE BY REMAINING CONTEXT. The freshest agent explores (wide reads, searches,
   debug loops). The most loaded agent judges (reviews, decides, holds the why).
   Run `relay.py roles`. As the fresh one loads up, the roles rotate.
3. DIGESTS, NOT STATE. Compare with `relay.py sync`, which hashes each dimension
   separately. Spend tokens only on dimensions that differ.
4. OLD OWNS WHY, FRESH OWNS WHAT. On a conflict about intent or rejected
   alternatives, the older agent wins. About current file state, the fresher wins.
   About a fact, neither wins -- run the verify command; reality wins.
5. PULL, NOT PUSH. A cell holds pointers, not pasted content. Let the reader decide
   what to spend its context on.

## Cycle

    python scripts/relay.py stamp <me> --context 0.55   # refresh my meta
    python scripts/relay.py check <me>                  # gate my own cell
    python scripts/relay.py sync                        # where do we differ?
    ... reconcile only the CONFLICT dimensions, anchored on the repo ...
    python scripts/relay.py resolve --dim "State" --winner <agent|repo> --note "..."

## Does this pay?

`relay.py report` reads divergence.jsonl and answers it. If after ~20 cycles the
agents rarely diverged, or diverged only on trivia, the error correction bought
nothing -- drop to a single-agent handoff and keep the orbit for high-stakes work.
That is the question this prototype exists to settle.
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%dT%H:%M:%S")


def git(root: Path, *args: str) -> str:
    try:
        out = subprocess.run(["git", *args], cwd=str(root), capture_output=True,
                             text=True, timeout=15)
        return out.stdout.strip() if out.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def head_sha(root: Path) -> str:
    return git(root, "rev-parse", "--short", "HEAD") or "nogit"


def find_root(start: Path) -> Path:
    for d in [start, *start.parents]:
        if (d / ".git").exists() or (d / "workflow").is_dir():
            return d
    return start


def relay_dir(root: Path) -> Path:
    return root / "workflow" / "relay"


# ---------------------------------------------------------------- parsing

def parse_meta(text: str) -> dict:
    m = META_RE.search(text)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta


def parse_sections(text: str) -> dict:
    """Split a cell into {section_name: [content lines]}."""
    body = META_RE.sub("", text)
    out, cur = {}, None
    for line in body.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return out


def normalize(lines) -> list:
    """Content lines, minus placeholders, blanks, and the 'none' sentinel."""
    keep = []
    for ln in lines:
        s = ln.strip()
        if not s or s.lower() == "none":
            continue
        if s.startswith("<") and s.endswith(">"):   # unfilled template hint
            continue
        keep.append(s)
    return keep


def dim_set(dim: str, lines) -> set:
    """Comparable unit for a dimension: tokens for capability lists, else lines."""
    n = normalize(lines)
    if dim in TOKEN_DIMS:
        return {t for ln in n for t in ln.replace(",", " ").split() if t}
    return set(n)


def digest_of(dim: str, lines) -> str:
    s = dim_set(dim, lines)
    if not s:
        return "empty"
    return hashlib.sha1("\n".join(sorted(s)).encode("utf-8", "replace")).hexdigest()[:10]


def cell_path(root: Path, agent: str) -> Path:
    safe = "".join(c if (c.isalnum() or c in "-_") else "_" for c in agent)
    return relay_dir(root) / "beliefs" / f"{safe}.md"


def load_cells(root: Path) -> dict:
    beliefs = relay_dir(root) / "beliefs"
    cells = {}
    if not beliefs.is_dir():
        return cells
    for p in sorted(beliefs.glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        meta = parse_meta(text)
        cells[meta.get("agent", p.stem)] = {
            "path": p, "meta": meta, "sections": parse_sections(text),
            "lines": len(text.splitlines()),
        }
    return cells


def age_min(meta: dict) -> float:
    try:
        t = datetime.strptime(meta.get("updated", ""), "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return 1e9
    return (datetime.now() - t).total_seconds() / 60.0


def load_profile(root: Path, harness: str) -> dict:
    p = relay_dir(root) / "profiles" / f"{harness}.md"
    if not p.exists():
        return {}
    m = PROFILE_RE.search(p.read_text(encoding="utf-8", errors="replace"))
    if not m:
        return {}
    parts = [x.strip() for x in m.group(1).strip().splitlines() if x.strip()]
    if len(parts) < 3:
        return {}
    return {"harness": parts[0],
            "shells": [s.strip() for s in parts[1].split(",") if s.strip()],
            "tools": [s.strip() for s in parts[2].split(",") if s.strip()]}


def jsonl_append(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=True) + "\n")


def jsonl_read(path: Path) -> list:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except ValueError:
                pass
    return out


# ---------------------------------------------------------------- commands

def cmd_init(root: Path, args) -> int:
    d = relay_dir(root)
    (d / "beliefs").mkdir(parents=True, exist_ok=True)
    (d / "profiles").mkdir(parents=True, exist_ok=True)
    readme = d / "README.md"
    if not readme.exists() or args.force:
        readme.write_text(README, encoding="utf-8")
    for name, body in PROFILES.items():
        p = d / "profiles" / f"{name}.md"
        if not p.exists() or args.force:
            p.write_text(
                f"<!-- relay:profile\n{body}\n-->\n# {name}\n\n"
                "Line 1 harness, line 2 shells, line 3 tools. `Requires:` in a belief\n"
                "cell is checked against line 3. Edit to match reality.\n",
                encoding="utf-8")
    print(f"[ok] relay initialized at {d}")
    return 0


def cmd_bootstrap(root: Path, args) -> int:
    path = cell_path(root, args.agent)
    if path.exists() and not args.force:
        print(f"[!!] {path} exists (use --force to overwrite)")
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(CELL_TEMPLATE.format(agent=args.agent, harness=args.harness,
                                         updated=now_iso(), head=head_sha(root),
                                         cap=LINE_CAP), encoding="utf-8")
    print(f"[ok] belief cell -> {path}")
    print("     fill it in, then: python scripts/relay.py check " + args.agent)
    return 0


def cmd_stamp(root: Path, args) -> int:
    path = cell_path(root, args.agent)
    if not path.exists():
        print(f"[!!] no cell for {args.agent}; run bootstrap first")
        return 1
    text = path.read_text(encoding="utf-8", errors="replace")
    meta = parse_meta(text)
    meta["agent"] = args.agent
    meta["updated"] = now_iso()
    meta["head"] = head_sha(root)
    if args.harness:
        meta["harness"] = args.harness
    if args.context is not None:
        meta["context"] = f"{max(0.0, min(1.0, args.context)):.2f}"
    block = "<!-- relay:meta\n" + "".join(
        f"{k}: {meta[k]}\n" for k in ("agent", "harness", "updated", "head", "context")
        if k in meta) + "-->"
    text = META_RE.sub(lambda _m: block, text, count=1) if META_RE.search(text) \
        else block + "\n" + text
    path.write_text(text, encoding="utf-8")
    print(f"[ok] {args.agent} stamped: head={meta['head']} context={meta.get('context','?')}")
    return 0


def cmd_check(root: Path, args) -> int:
    path = cell_path(root, args.agent)
    if not path.exists():
        print(f"[!!] no cell for {args.agent}")
        return 1
    text = path.read_text(encoding="utf-8", errors="replace")
    meta, sections = parse_meta(text), parse_sections(text)
    fails, warns = [], []

    for k in ("agent", "harness", "updated", "head"):
        if not meta.get(k):
            fails.append(f"meta missing '{k}'")
    for dim in REQUIRED:
        if dim not in sections:
            fails.append(f"missing section '## {dim}'")
        elif dim in SINGULAR and not normalize(sections[dim]):
            fails.append(f"section '{dim}' is empty or still a template hint")

    n_lines = len(text.splitlines())
    if n_lines > LINE_CAP:
        fails.append(f"cell is {n_lines} lines (cap {LINE_CAP}) -- it is becoming a transcript")

    cur = head_sha(root)
    if meta.get("head") and meta["head"] != cur and not args.allow_stale:
        fails.append(f"STALE: cell stamped at {meta['head']}, repo HEAD is {cur} "
                     "-- re-derive from the repo, do not trust this cell")

    anchor = " ".join(sections.get("Anchor", [])).strip()
    if "verify:" not in anchor:
        warns.append("no 'verify:' command in ## Anchor -- nothing proves State is true")

    prof = load_profile(root, meta.get("harness", ""))
    missing = []
    if prof:
        have = set(prof["tools"])
        for req in normalize(sections.get("Requires", [])):
            for tok in (t.strip() for t in req.replace(",", " ").split()):
                if tok and tok not in have:
                    missing.append(tok)
        if missing:
            fails.append(f"harness '{meta.get('harness')}' lacks: {', '.join(sorted(set(missing)))}"
                         " -- stop and report, do not substitute")
    else:
        warns.append(f"no profile for harness '{meta.get('harness','?')}' -- capability gap unchecked")

    result = {"agent": args.agent, "pass": not fails, "lines": n_lines,
              "head": meta.get("head"), "repo_head": cur,
              "fails": fails, "warns": warns}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"-- check {args.agent} --")
        for w in warns:
            print(f"  [warn] {w}")
        for f in fails:
            print(f"  [FAIL] {f}")
        print(f"  {'[ok] PASS' if not fails else '[!!] FAIL'}  ({n_lines}/{LINE_CAP} lines)")
    return 0 if not fails else 1


def compare(cells: dict) -> list:
    """Per-dimension comparison across all cells. The Merkle-ish cheap surface."""
    names = sorted(cells)
    rows = []
    for dim in DIMENSIONS:
        sets = {n: dim_set(dim, cells[n]["sections"].get(dim, [])) for n in names}
        digs = {n: digest_of(dim, cells[n]["sections"].get(dim, [])) for n in names}
        if len({tuple(sorted(s)) for s in sets.values()}) == 1:
            rows.append({"dim": dim, "status": "SYNC", "digests": digs, "detail": ""})
            continue
        status, detail = "CONFLICT", ""
        if dim in LIST:
            union = set().union(*sets.values())
            supersets = [n for n in names if sets[n] == union]
            if supersets:                       # everyone else is a subset -> catch-up
                behind = [n for n in names if sets[n] != union]
                status = "GAP"
                detail = f"{supersets[0]} ahead; behind: {', '.join(behind)}"
        if status == "CONFLICT":
            diffs = []
            for n in names:
                only = sets[n] - set().union(*[sets[o] for o in names if o != n])
                if only:
                    diffs.append(f"{n} only: " + "; ".join(sorted(only))[:120])
            detail = " | ".join(diffs)
        rows.append({"dim": dim, "status": status, "digests": digs, "detail": detail})
    return rows


def cmd_sync(root: Path, args) -> int:
    cells = load_cells(root)
    if len(cells) < 2:
        print(f"[!!] need 2+ belief cells to compare (found {len(cells)})")
        return 1
    rows = compare(cells)
    names = sorted(cells)
    heads = {c["meta"].get("head") for c in cells.values()}
    cur = head_sha(root)
    conflicts = [r for r in rows if r["status"] == "CONFLICT"]

    if args.json:
        print(json.dumps({"agents": names, "repo_head": cur,
                          "anchored": heads == {cur}, "rows": rows}, indent=2))
        return 1 if conflicts else 0

    print(f"-- sync: {', '.join(names)} --")
    if heads != {cur}:
        print(f"  [warn] cells are not all anchored at HEAD {cur}: "
              + ", ".join(f"{n}={cells[n]['meta'].get('head')}" for n in names))
        print("         re-derive from the repo before trusting any comparison below")
    print()
    print("  {:<16} {:<9} {}".format("DIMENSION", "STATUS", "DETAIL"))
    for r in rows:
        mark = {"SYNC": "  ", "GAP": "> ", "CONFLICT": "!!"}[r["status"]]
        print("{} {:<16} {:<9} {}".format(mark, r["dim"], r["status"], r["detail"][:90]))
    print()
    if conflicts:
        print("  Reconcile ONLY the CONFLICT rows. Tiebreak:")
        print("    fact         -> run the verify command; reality wins")
        print("    why/intent   -> the OLDER agent wins (most history)")
        print("    file state   -> the FRESHER agent wins (just read it)")
        print("  Then: relay.py resolve --dim \"<dim>\" --winner <agent|repo> --note \"...\"")
    else:
        print("  [ok] no conflicts -- spend nothing here")
    return 1 if conflicts else 0


def cmd_roles(root: Path, args) -> int:
    cells = load_cells(root)
    if not cells:
        print("[!!] no belief cells")
        return 1
    live, offline = [], []
    for n, c in cells.items():
        try:
            ctx = float(c["meta"].get("context", "0"))
        except ValueError:
            ctx = 0.0
        rec = {"agent": n, "harness": c["meta"].get("harness", "?"),
               "context": ctx, "age_min": round(age_min(c["meta"]), 1)}
        (offline if rec["age_min"] > args.stale_after else live).append(rec)
    live.sort(key=lambda r: r["context"])
    for i, r in enumerate(live):
        # One live agent is not an orbit -- do not hand it both roles.
        r["role"] = "SOLO" if len(live) == 1 else (
            "EXPLORER" if i == 0 else ("JUDGE" if i == len(live) - 1 else "SECOND"))
    if args.json:
        print(json.dumps({"live": live, "offline": offline}, indent=2))
        return 0
    print("-- roles (by remaining context) --")
    for r in live:
        bar = "#" * int(r["context"] * 20)
        print("  {:<8} {:<18} {:<12} [{:<20}] {:>3.0f}% used, {:.0f}m ago".format(
            r["role"], r["agent"], r["harness"], bar, r["context"] * 100, r["age_min"]))
    for r in offline:
        print("  {:<8} {:<18} {:<12} (last stamp {:.0f}m ago)".format(
            "OFFLINE", r["agent"], r["harness"], r["age_min"]))
    print()
    if len(live) == 1:
        print(f"  SOLO ({live[0]['agent']}): no orbit -- nothing is checking this agent.")
        print("  Stamp a second agent, or accept single-agent handoff for this stretch.")
    elif live:
        print(f"  EXPLORER ({live[0]['agent']}): wide reads, searches, debug loops.")
        print(f"  JUDGE    ({live[-1]['agent']}): review, decide, hold the why. No big reads.")
    else:
        print("  No live agents -- every cell is stale. Re-derive from the repo.")
    return 0


def cmd_note(root: Path, args) -> int:
    rec = {"ts": now_iso(), "agent": args.agent, "kind": args.kind,
           "head": head_sha(root), "text": args.text}
    jsonl_append(relay_dir(root) / "journal.jsonl", rec)
    print(f"[ok] journal += {args.kind} ({args.agent})")
    return 0


def cmd_resolve(root: Path, args) -> int:
    rec = {"ts": now_iso(), "dim": args.dim, "type": args.type, "winner": args.winner,
           "head": head_sha(root), "note": args.note or ""}
    jsonl_append(relay_dir(root) / "divergence.jsonl", rec)
    print(f"[ok] divergence += {args.dim} -> {args.winner}")
    return 0


def cmd_status(root: Path, args) -> int:
    cells = load_cells(root)
    d = relay_dir(root)
    div, jour = jsonl_read(d / "divergence.jsonl"), jsonl_read(d / "journal.jsonl")
    if args.json:
        print(json.dumps({
            "repo_head": head_sha(root), "agents": sorted(cells),
            "divergences": len(div), "journal_entries": len(jour),
            "conflicts_open": sum(1 for r in compare(cells) if r["status"] == "CONFLICT")
            if len(cells) > 1 else 0}, indent=2))
        return 0
    print(f"-- relay status ({d}) --")
    print(f"  repo HEAD      : {head_sha(root)}")
    print(f"  belief cells   : {len(cells)} ({', '.join(sorted(cells)) or 'none'})")
    print(f"  journal        : {len(jour)} entries")
    print(f"  divergences    : {len(div)} recorded")
    if len(cells) > 1:
        rows = compare(cells)
        c = sum(1 for r in rows if r["status"] == "CONFLICT")
        g = sum(1 for r in rows if r["status"] == "GAP")
        print(f"  live comparison: {c} conflict(s), {g} gap(s)  -> relay.py sync")
    return 0


def cmd_report(root: Path, args) -> int:
    """The instrument: is the orbit earning its 2-3x token cost?"""
    div = jsonl_read(relay_dir(root) / "divergence.jsonl")
    by_dim, by_winner, by_type = {}, {}, {}
    for r in div:
        by_dim[r.get("dim", "?")] = by_dim.get(r.get("dim", "?"), 0) + 1
        by_winner[r.get("winner", "?")] = by_winner.get(r.get("winner", "?"), 0) + 1
        by_type[r.get("type", "?")] = by_type.get(r.get("type", "?"), 0) + 1
    substantive = sum(v for k, v in by_dim.items() if k in SINGULAR)
    if args.json:
        print(json.dumps({"total": len(div), "substantive": substantive,
                          "by_dim": by_dim, "by_winner": by_winner,
                          "by_type": by_type}, indent=2))
        return 0
    print("-- divergence report --")
    print(f"  recorded divergences : {len(div)}")
    print(f"  substantive          : {substantive}  (on {', '.join(SINGULAR)})")
    for title, table in (("by dimension", by_dim), ("by winner", by_winner),
                         ("by type", by_type)):
        if table:
            print(f"  {title}:")
            for k, v in sorted(table.items(), key=lambda kv: -kv[1]):
                print(f"    {k:<18} {v}")
    print()
    if len(div) < 20:
        print(f"  [--] {len(div)}/20 cycles logged. Not enough to judge the orbit yet.")
    elif substantive == 0:
        print("  [!!] Zero substantive divergence over 20+ cycles. The orbit is not")
        print("       buying error correction. Drop to single-agent handoff.")
    else:
        rate = 100.0 * substantive / max(1, len(div))
        print(f"  [ok] {rate:.0f}% of divergences were substantive. The orbit is catching")
        print("       real disagreement -- keep it for work at this stakes level.")
        top = max(by_winner.items(), key=lambda kv: kv[1]) if by_winner else None
        if top and top[1] > len(div) * 0.6 and top[0] != "repo":
            print(f"  [!!] '{top[0]}' won {top[1]}/{len(div)}. That is not a handoff finding,")
            print("       that is a finding about which agent to trust for this work.")
    return 0


def cmd_dispatch(root: Path, args) -> int:
    """Paste-able boot block. No slash commands, no skills, no MCP -- portable."""
    cells = load_cells(root)
    others = [n for n in sorted(cells) if n != args.agent]
    path = cell_path(root, args.agent).relative_to(root).as_posix()
    print("-" * 74)
    print(f"cd {root}")
    print()
    print(f"You are agent '{args.agent}' in a relay orbit with: "
          f"{', '.join(others) if others else '(none yet -- you are first)'}.")
    print("Read workflow/relay/README.md for the protocol, then:")
    print()
    print(f"  1. python scripts/relay.py bootstrap {args.agent} --harness <your harness>")
    print(f"     (skip if {path} already exists -- read it instead)")
    print("  2. Re-derive the true state from the repo: git status, git log -5,")
    print("     and the verify command in the other agents' ## Anchor sections.")
    print("     Anchor on the repo, NOT on what another agent's cell claims.")
    print(f"  3. Fill in {path} with YOUR OWN view. Do not copy another cell --")
    print("     independent derivation is the only thing that makes agreement mean")
    print("     anything. Pointers, not pasted content. Under 150 lines.")
    print(f"  4. python scripts/relay.py stamp {args.agent} --context <0.0-1.0 used>")
    print(f"  5. python scripts/relay.py check {args.agent}")
    print("  6. python scripts/relay.py sync")
    print("  7. Reconcile ONLY the CONFLICT dimensions. Record each one:")
    print("     python scripts/relay.py resolve --dim \"<dim>\" --winner <agent|repo> --note \"...\"")
    print("  8. python scripts/relay.py roles   -- then do the work that role calls for.")
    print()
    print("Stop after step 8 and report. Do not start building before the sync is clean.")
    print("-" * 74)
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="relay.py", description=__doc__.split("\n")[0])
    p.add_argument("--root", default=None, help="repo root (default: auto-detect)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init"); s.add_argument("--force", action="store_true")
    s = sub.add_parser("bootstrap")
    s.add_argument("agent"); s.add_argument("--harness", default="unknown")
    s.add_argument("--force", action="store_true")
    s = sub.add_parser("stamp")
    s.add_argument("agent"); s.add_argument("--context", type=float, default=None)
    s.add_argument("--harness", default=None)
    s = sub.add_parser("check")
    s.add_argument("agent"); s.add_argument("--json", action="store_true")
    s.add_argument("--allow-stale", action="store_true")
    s = sub.add_parser("sync"); s.add_argument("--json", action="store_true")
    s = sub.add_parser("roles")
    s.add_argument("--json", action="store_true")
    s.add_argument("--stale-after", type=float, default=STALE_AFTER_MIN)
    s = sub.add_parser("note")
    s.add_argument("agent")
    s.add_argument("--kind", required=True,
                   choices=["decision", "dead-end", "finding", "blocked"])
    s.add_argument("--text", required=True)
    s = sub.add_parser("resolve")
    s.add_argument("--dim", required=True); s.add_argument("--winner", required=True)
    s.add_argument("--type", default="conflict", choices=["conflict", "gap"])
    s.add_argument("--note", default="")
    s = sub.add_parser("status"); s.add_argument("--json", action="store_true")
    s = sub.add_parser("report"); s.add_argument("--json", action="store_true")
    s = sub.add_parser("dispatch"); s.add_argument("agent")

    args = p.parse_args()
    root = Path(args.root).resolve() if args.root else find_root(Path.cwd())
    return globals()[f"cmd_{args.cmd.replace('-', '_')}"](root, args)


if __name__ == "__main__":
    sys.exit(main())
