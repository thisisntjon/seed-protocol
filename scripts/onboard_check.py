#!/usr/bin/env python3
"""onboard_check.py -- verifies the skeleton's documentation against reality (Law 1).

Checks:
  1. PATHS      every path claimed in START-HERE.md's file map exists
  2. RETRACT    no retracted token (workflow/canon/RETRACTIONS.md) cited outside the ledger
  3. GATES      no OPEN gate in GATES.md older than the SLA; no DEFERRED gate past its date
  4. RECEIPTS   every file in workflow/receipts/ carries STATE / EVIDENCE / NEXT_OWNER

Exit 0 = documentation is trustworthy. Exit 1 = something above is lying; fix before acting.
ASCII output only (Windows cp1252 console crash is a documented origin-corpus incident).
"""
import argparse
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

SLA_HOURS = 48
TRACKED_GLOBS = ["*.md", "workflow/**/*.md"]

def fail(msgs, text):
    msgs.append("ERROR   " + text)

def note(msgs, text):
    msgs.append("warn    " + text)

def check_paths(root, msgs):
    src = root / "START-HERE.md"
    if not src.exists():
        fail(msgs, "START-HERE.md missing -- the skeleton has no front door")
        return
    tokens = re.findall(r"`([^`\n]+)`", src.read_text(encoding="utf-8"))
    for tok in tokens:
        if " " in tok or "*" in tok or tok.startswith("http"):
            continue
        if not ("/" in tok or "\\" in tok or tok.endswith((".md", ".py"))):
            continue
        p = root / tok.rstrip("/")
        if not p.exists():
            fail(msgs, f"START-HERE.md claims `{tok}` but it does not exist")

def parse_table_rows(text, id_prefix=None):
    rows = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or set(cells[0]) <= {"-", " ", ":"}:
            continue
        if id_prefix and not cells[0].startswith(id_prefix):
            continue
        rows.append(cells)
    return rows

def check_retractions(root, msgs):
    ledger = root / "workflow" / "canon" / "RETRACTIONS.md"
    if not ledger.exists():
        fail(msgs, "workflow/canon/RETRACTIONS.md missing")
        return
    tokens = []
    for cells in parse_table_rows(ledger.read_text(encoding="utf-8")):
        if cells[0] in ("token",):
            continue
        tokens.append(cells[0])
    if not tokens:
        return
    files = set()
    for g in TRACKED_GLOBS:
        files.update(root.glob(g))
    for f in sorted(files):
        if f.resolve() == ledger.resolve() or not f.is_file():
            continue
        body = f.read_text(encoding="utf-8", errors="replace")
        for tok in tokens:
            if tok and tok in body:
                fail(msgs, f"retracted token '{tok}' cited in {f.relative_to(root)} "
                           f"-- check the ledger, use the replacement")

def check_gates(root, msgs, now=None):
    gates = root / "GATES.md"
    if not gates.exists():
        fail(msgs, "GATES.md missing -- the human-key boundary is undefined")
        return
    now = now or datetime.now()
    open_count = 0
    for cells in parse_table_rows(gates.read_text(encoding="utf-8"), id_prefix="G-"):
        if len(cells) < 5:
            fail(msgs, f"gate row malformed (need 5 cells): {cells}")
            continue
        gid, what, _owner, opened_s, status = cells[0], cells[1], cells[2], cells[3], cells[4]
        try:
            opened = datetime.strptime(opened_s, "%Y-%m-%d")
        except ValueError:
            fail(msgs, f"gate {gid}: opened date '{opened_s}' not YYYY-MM-DD")
            continue
        if status.upper().startswith("OPEN"):
            open_count += 1
            age = now - opened
            if age > timedelta(hours=SLA_HOURS):
                fail(msgs, f"gate {gid} OPEN for {age.days}d ({what[:60]}) -- SLA is {SLA_HOURS}h. "
                           f"Pending gates kill projects: answer it or defer it with a date.")
        elif status.upper().startswith("DEFERRED"):
            m = re.search(r"DEFERRED\((\d{4}-\d{2}-\d{2})\)", status)
            if not m:
                fail(msgs, f"gate {gid}: DEFERRED requires a revisit date, e.g. DEFERRED(2026-09-01)")
            elif datetime.strptime(m.group(1), "%Y-%m-%d") < now:
                fail(msgs, f"gate {gid}: deferral date {m.group(1)} has passed -- re-decide it")
    if open_count:
        note(msgs, f"{open_count} gate(s) OPEN and inside SLA -- fine, but they are on the clock")

def check_receipts(root, msgs):
    rdir = root / "workflow" / "receipts"
    if not rdir.exists():
        fail(msgs, "workflow/receipts/ missing")
        return
    required = ("STATE:", "EVIDENCE:", "NEXT_OWNER:")
    for f in sorted(rdir.glob("*.md")):
        body = f.read_text(encoding="utf-8", errors="replace")
        missing = [k for k in required if k not in body]
        if missing:
            fail(msgs, f"receipt {f.name} missing field(s): {', '.join(missing)} "
                       f"-- 'done' without evidence is not a state")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="repo root (default: parent of this script)")
    args = ap.parse_args()
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    msgs = []
    check_paths(root, msgs)
    check_retractions(root, msgs)
    check_gates(root, msgs)
    check_receipts(root, msgs)
    errors = [m for m in msgs if m.startswith("ERROR")]
    warns = [m for m in msgs if m.startswith("warn")]
    for m in msgs:
        print(m)
    print(f"\n{len(errors)} error(s), {len(warns)} warning(s). "
          + ("ONBOARD CHECK PASSED" if not errors else "ONBOARD CHECK FAILED -- docs are lying somewhere"))
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
