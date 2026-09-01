#!/usr/bin/env python3
"""relay_selftest.py -- end-to-end proof that the relay buffer detects what it claims.

Builds a throwaway git repo, runs two agents through a full orbit cycle via the
real CLI (subprocess, not imports), and asserts on both directions:

  POSITIVE  seeded divergence is detected and correctly classified
  NEGATIVE  identical cells raise nothing (no false alarms)

ASCII output only. Exit 0 = all cases pass.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RELAY = Path(__file__).resolve().parent / "relay.py"
PASS, FAIL = [], []


def run(root: Path, *args, expect=None):
    r = subprocess.run([sys.executable, str(RELAY), "--root", str(root), *args],
                       capture_output=True, text=True)
    if expect is not None and r.returncode != expect:
        FAIL.append(f"exit {r.returncode} != {expect} for: {' '.join(args)}\n{r.stdout}{r.stderr}")
    return r


def case(name: str, ok: bool, detail: str = ""):
    (PASS if ok else FAIL).append(name if ok else f"{name} :: {detail}")
    print(f"  [{'ok' if ok else '!!'}] {name}" + ("" if ok else f"  <- {detail}"))


def cell(objective, state, nxt, dead, questions, requires="git", harness="claude-code",
         agent="a", head="HEAD", verify="python scripts/relay.py status",
         updated="2099-01-01T00:00:00"):
    return f"""<!-- relay:meta
agent: {agent}
harness: {harness}
updated: {updated}
head: {head}
context: 0.10
-->
# Belief -- {agent}

## Objective
{objective}

## State
{state}

## Next action
{nxt}

## Dead ends
{dead}

## Open questions
{questions}

## Binding rules
none

## Requires
{requires}

## Anchor
verify: {verify}
"""


def write(root: Path, agent: str, text: str):
    (root / "workflow" / "relay" / "beliefs" / f"{agent}.md").write_text(text, encoding="utf-8")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="relay-selftest-"))
    try:
        for c in (["git", "init", "-q"], ["git", "config", "user.email", "t@t"],
                  ["git", "config", "user.name", "t"]):
            subprocess.run(c, cwd=str(tmp), capture_output=True)
        (tmp / "seed.txt").write_text("seed\n", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=str(tmp), capture_output=True)
        subprocess.run(["git", "commit", "-qm", "seed"], cwd=str(tmp), capture_output=True)
        head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(tmp),
                              capture_output=True, text=True).stdout.strip()

        print("-- setup --")
        run(tmp, "init", expect=0)
        case("init scaffolds relay dir", (tmp / "workflow" / "relay" / "profiles" /
                                          "claude-code.md").exists())
        run(tmp, "bootstrap", "a", "--harness", "claude-code", expect=0)
        case("bootstrap creates a cell",
             (tmp / "workflow" / "relay" / "beliefs" / "a.md").exists())
        r = run(tmp, "check", "a")
        case("fresh template FAILS the gate (unfilled sections)", r.returncode == 1,
             "an empty template must not pass")

        print("\n-- NEGATIVE control: identical cells --")
        base = dict(objective="Ship the relay prototype.", state="clean at HEAD",
                    nxt="run the selftest", dead="tried X, fails on Y",
                    questions="does the orbit pay?", head=head)
        write(tmp, "a", cell(agent="a", **base))
        write(tmp, "b", cell(agent="b", **base))
        r = run(tmp, "sync", "--json")
        rows = json.loads(r.stdout)["rows"]
        bad = [x["dim"] for x in rows if x["status"] != "SYNC"]
        case("identical cells -> 0 false alarms", not bad, f"flagged {bad}")
        case("sync exits 0 when clean", r.returncode == 0)

        print("\n-- POSITIVE: seeded divergence --")
        write(tmp, "b", cell(agent="b", objective="Ship the relay prototype.",
                             state="dirty: three files mid-edit",   # SINGULAR conflict
                             nxt="run the selftest",
                             dead="tried X, fails on Y\ntried Z, also fails",  # LIST gap
                             questions="does the orbit pay?", head=head))
        r = run(tmp, "sync", "--json")
        rows = {x["dim"]: x for x in json.loads(r.stdout)["rows"]}
        case("differing State -> CONFLICT", rows["State"]["status"] == "CONFLICT",
             rows["State"]["status"])
        case("superset Dead ends -> GAP (not conflict)",
             rows["Dead ends"]["status"] == "GAP", rows["Dead ends"]["status"])
        case("untouched dims stay SYNC", rows["Objective"]["status"] == "SYNC"
             and rows["Next action"]["status"] == "SYNC")
        case("conflict detail names the dissenter", "b" in rows["State"]["detail"],
             rows["State"]["detail"])
        case("sync exits 1 on conflict", r.returncode == 1)

        print("\n-- regressions caught by the first live run --")
        # Token lists were compared line-wise, so "git python" vs "git python mcp:x"
        # read as CONFLICT when it is plainly a GAP.
        write(tmp, "a", cell(agent="a", requires="git python", **base))
        write(tmp, "b", cell(agent="b", requires="git python mcp:local-memory", **base))
        rows = {x["dim"]: x for x in json.loads(run(tmp, "sync", "--json").stdout)["rows"]}
        case("Requires compared token-wise -> GAP, not CONFLICT",
             rows["Requires"]["status"] == "GAP", rows["Requires"]["status"])
        write(tmp, "b", cell(agent="b", requires="git python", **base))
        case("identical token lists -> SYNC",
             {x["dim"]: x for x in json.loads(run(tmp, "sync", "--json").stdout)["rows"]
              }["Requires"]["status"] == "SYNC")
        # One live agent was being handed EXPLORER and JUDGE simultaneously.
        write(tmp, "b", cell(agent="b", updated="2020-01-01T00:00:00", **base))
        run(tmp, "stamp", "a", "--context", "0.40", expect=0)
        live = json.loads(run(tmp, "roles", "--json").stdout)["live"]
        case("one live agent -> SOLO, not both roles",
             len(live) == 1 and live[0]["role"] == "SOLO", json.dumps(live))
        case("SOLO output says nothing is checking it",
             "no orbit" in run(tmp, "roles").stdout)

        print("\n-- self-invalidation --")
        write(tmp, "a", cell(agent="a", head="deadbee", **{k: v for k, v in base.items()
                                                           if k != "head"}))
        r = run(tmp, "check", "a")
        case("stale head -> FAIL", r.returncode == 1 and "STALE" in r.stdout)
        r = run(tmp, "check", "a", "--allow-stale")
        case("--allow-stale overrides", r.returncode == 0, r.stdout)
        r = run(tmp, "sync")
        case("sync warns when cells are not all at HEAD", "not all anchored" in r.stdout)

        print("\n-- impedance match --")
        write(tmp, "a", cell(agent="a", harness="codex", requires="git mcp:local-memory",
                             **base))
        r = run(tmp, "check", "a")
        case("capability gap -> FAIL", r.returncode == 1 and "mcp:local-memory" in r.stdout,
             r.stdout)
        case("gap message forbids substitution", "do not substitute" in r.stdout)
        write(tmp, "a", cell(agent="a", harness="claude-code",
                             requires="git mcp:local-memory", **base))
        case("same requirement passes on a harness that has it",
             run(tmp, "check", "a").returncode == 0)

        print("\n-- size cap --")
        write(tmp, "a", cell(agent="a", **base) + "\nfiller\n" * 200)
        r = run(tmp, "check", "a")
        case("oversized cell -> FAIL (it is becoming a transcript)",
             r.returncode == 1 and "transcript" in r.stdout)
        write(tmp, "a", cell(agent="a", **base))

        print("\n-- role rotation --")
        run(tmp, "stamp", "a", "--context", "0.82", expect=0)
        run(tmp, "stamp", "b", "--context", "0.15", expect=0)
        roles = {x["agent"]: x["role"] for x in json.loads(
            run(tmp, "roles", "--json").stdout)["live"]}
        case("loaded agent judges", roles.get("a") == "JUDGE", str(roles))
        case("fresh agent explores", roles.get("b") == "EXPLORER", str(roles))
        run(tmp, "stamp", "a", "--context", "0.05", expect=0)
        run(tmp, "stamp", "b", "--context", "0.90", expect=0)
        roles = {x["agent"]: x["role"] for x in json.loads(
            run(tmp, "roles", "--json").stdout)["live"]}
        case("roles ROTATE when context flips",
             roles.get("a") == "EXPLORER" and roles.get("b") == "JUDGE", str(roles))

        print("\n-- ledgers --")
        run(tmp, "note", "a", "--kind", "dead-end", "--text", "tried Z, fails on W", expect=0)
        run(tmp, "resolve", "--dim", "State", "--winner", "repo", "--note", "ran verify", expect=0)
        rep = json.loads(run(tmp, "report", "--json").stdout)
        case("divergence recorded and counted as substantive",
             rep["total"] == 1 and rep["substantive"] == 1, json.dumps(rep))
        case("journal appended", (tmp / "workflow" / "relay" / "journal.jsonl").exists())
        for _ in range(20):
            run(tmp, "resolve", "--dim", "Requires", "--winner", "a", "--type", "gap")
        out = run(tmp, "report").stdout
        case("report calls out a dominant winner", "which agent to trust" in out, out)

        print("\n-- portability --")
        out = run(tmp, "dispatch", "b").stdout
        lines = [ln.strip() for ln in out.splitlines()]
        case("dispatch block is harness-neutral (no slash commands, skills, or MCP)",
             not any(ln.startswith("/") for ln in lines)
             and "skill" not in out.lower() and "mcp__" not in out
             and "python scripts/relay.py" in out,
             next((ln for ln in lines if ln.startswith("/")), "skill/mcp reference"))
        case("dispatch forbids copying another cell", "Do not copy another cell" in out)
        blob = (RELAY.read_text(encoding="utf-8")
                + (tmp / "workflow" / "relay" / "README.md").read_text(encoding="utf-8"))
        case("outputs are ASCII-only (cp1252 incident)", blob.isascii())

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"\n{'=' * 60}\n{len(PASS)} passed, {len(FAIL)} failed")
    for f in FAIL:
        print(f"  FAIL: {f}")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    sys.exit(main())
