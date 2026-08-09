#!/usr/bin/env python3
"""spend_check.py -- Law 9: spend must convert to closed loops.

Incident this encodes: ~$49,686 API-list-equivalent compute was consumed across the surviving
transcript window while the campaign's own verdict was "zero confirmed agent improvements",
and the project's COST.md was empty checkboxes. Unmeasured spend with no consumption test is
the failure mode; this check makes it impossible to repeat silently.

Reads the newest ccusage JSON export (the metering instrument), sums window spend, counts
closed loops from workflow/receipts (DONE with PROGRESS decision/measurement, or KILLED --
a kill on evidence is a closed loop), and FAILS when spend exceeds the threshold with zero
loops closed. A missing or stale export is itself a failure: unmetered spend is the incident.

All dollar figures are API-LIST-EQUIVALENT (token counts x list prices), not subscription cash.
ASCII output only. --selftest proves refutation power (Law 2) before green is trusted.
"""
import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_DATA_DIR = Path.home() / ".claude" / "planning" / "refinery" / "data"
CLOSED_STATES_PROGRESS = {"DECISION", "MEASUREMENT"}


def parse_fields(body):
    fields = {}
    for line in body.splitlines():
        match = re.match(r"^([A-Z][A-Z0-9_]*):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def newest_export(data_dir):
    candidates = sorted(data_dir.glob("ccusage-*.json")) if data_dir.exists() else []
    return candidates[-1] if candidates else None


def window_spend(export_path, window_days):
    data = json.loads(export_path.read_text(encoding="utf-8"))
    daily = data.get("daily", [])
    if not daily:
        return None, None, None
    periods = sorted(row["period"] for row in daily if "period" in row)
    end = datetime.strptime(periods[-1], "%Y-%m-%d")
    start = end - timedelta(days=window_days - 1)
    spend = sum(
        row.get("totalCost", 0.0)
        for row in daily
        if "period" in row and start <= datetime.strptime(row["period"], "%Y-%m-%d") <= end
    )
    return spend, start, end


def closed_loops(receipts_dir, start, end):
    loops = []
    if not receipts_dir.exists():
        return loops
    for path in sorted(receipts_dir.glob("*.md")):
        m = re.match(r"(\d{4}-\d{2}-\d{2})", path.name)
        if not m:
            continue
        when = datetime.strptime(m.group(1), "%Y-%m-%d")
        if not (start <= when <= end):
            continue
        fields = parse_fields(path.read_text(encoding="utf-8", errors="replace"))
        state = fields.get("STATE", "").upper()
        progress = fields.get("PROGRESS", "").upper()
        if state == "KILLED" or (state == "DONE" and progress in CLOSED_STATES_PROGRESS):
            loops.append(path.name)
    return loops


def evaluate(spend, loop_count, threshold):
    """Pure verdict logic, selftest target. Returns (ok, message)."""
    if spend >= threshold and loop_count == 0:
        return False, (
            f"ERROR   ${spend:,.2f} API-list-equivalent spent in window with ZERO closed loops "
            f"(threshold ${threshold:,.2f}). Throughput is not progress -- close a loop or stop."
        )
    if loop_count:
        return True, f"ok      ${spend:,.2f} spent / {loop_count} closed loop(s) = ${spend / loop_count:,.2f} per loop"
    return True, f"ok      ${spend:,.2f} spent, below threshold with no loops -- acceptable idle"


def check_freshness(export_path, max_age_days, now=None):
    """Stale metering is unmetered spend. Returns (ok, message)."""
    now = now or datetime.now()
    m = re.search(r"ccusage-(\d{4}-\d{2}-\d{2})", export_path.name)
    stamp = datetime.strptime(m.group(1), "%Y-%m-%d") if m else datetime.fromtimestamp(export_path.stat().st_mtime)
    age = (now - stamp).days
    if age > max_age_days:
        return False, (
            f"ERROR   newest usage export is {age}d old (max {max_age_days}d). Unmetered spend "
            f"is the incident this check exists for. Run: npx ccusage@latest daily --json "
            f"--sections daily,session > {DEFAULT_DATA_DIR}\\ccusage-YYYY-MM-DD.json"
        )
    return True, f"ok      usage export is {age}d old (max {max_age_days}d)"


def selftest():
    cases = [
        ("high spend + zero loops FAILS", not evaluate(150.0, 0, 100.0)[0]),
        ("high spend + loops passes", evaluate(150.0, 2, 100.0)[0]),
        ("low spend + zero loops passes", evaluate(10.0, 0, 100.0)[0]),
        ("stale export FAILS", not check_freshness(
            Path("ccusage-2026-01-01.json"), 7, now=datetime(2026, 8, 8))[0]),
        ("fresh export passes", check_freshness(
            Path("ccusage-2026-08-08.json"), 7, now=datetime(2026, 8, 8))[0]),
    ]
    ok = True
    for name, passed in cases:
        print(("PASS    " if passed else "FAIL    ") + name)
        ok = ok and passed
    print("\nSPEND CHECK SELFTEST " + ("PASSED -- the guard refutes its defects"
                                       if ok else "FAILED -- do not trust green"))
    return 0 if ok else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None, help="repo root (default: parent of this script)")
    parser.add_argument("--json", default=None, help="ccusage export path (default: newest in data dir)")
    parser.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR))
    parser.add_argument("--window-days", type=int, default=7)
    parser.add_argument("--max-unconsumed-usd", type=float, default=100.0,
                        help="window spend at/above this with zero closed loops = failure")
    parser.add_argument("--max-export-age-days", type=int, default=7)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    export = Path(args.json) if args.json else newest_export(Path(args.data_dir))
    if not export or not export.exists():
        print(f"ERROR   no usage export found in {args.data_dir} -- unmetered spend is the "
              f"incident this check exists for. Run: npx ccusage@latest daily --json "
              f"--sections daily,session > {args.data_dir}\\ccusage-YYYY-MM-DD.json")
        return 1
    ok_fresh, msg = check_freshness(export, args.max_export_age_days)
    print(msg)
    spend, start, end = window_spend(export, args.window_days)
    if spend is None:
        print("ERROR   export has no daily rows -- metering instrument is broken")
        return 1
    loops = closed_loops(root / "workflow" / "receipts", start, end)
    print(f"window  {start:%Y-%m-%d}..{end:%Y-%m-%d} ({args.window_days}d) from {export.name}")
    for name in loops:
        print(f"loop    {name}")
    ok_spend, msg = evaluate(spend, len(loops), args.max_unconsumed_usd)
    print(msg)
    print("\nSPEND CHECK " + ("PASSED" if ok_fresh and ok_spend else "FAILED"))
    return 0 if ok_fresh and ok_spend else 1


if __name__ == "__main__":
    sys.exit(main())
