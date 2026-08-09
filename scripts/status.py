#!/usr/bin/env python3
"""status.py -- one-glance progress for a SEED project.

Renders a progress bar computed from the Phasing table in workflow/PLAN.md (single source of
truth -- no separate state file to drift), plus gate pressure, receipts, and last checkpoint.

Status tokens in the PLAN's Status column: DONE | ACTIVE | ACTIVE(nn%) | TODO
ASCII output only (the origin corpus's cp1252 console crash is a documented incident).
"""
import argparse
import re
import subprocess
from datetime import datetime
from pathlib import Path

BAR_WIDTH = 30

def parse_rows(text, prefix):
    rows = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0].startswith(prefix) and not set(cells[0]) <= {"-", " ", ":"}:
            rows.append(cells)
    return rows

def phase_progress(root):
    plan = root / "workflow" / "PLAN.md"
    if not plan.exists():
        return None, []
    phases = []
    for cells in parse_rows(plan.read_text(encoding="utf-8"), "P"):
        if len(cells) < 4 or not re.match(r"P\d", cells[0]):
            continue
        status = cells[3].upper()
        if status.startswith("DONE"):
            frac = 1.0
        elif status.startswith("ACTIVE"):
            m = re.search(r"\((\d+)%\)", status)
            frac = (int(m.group(1)) / 100) if m else 0.25
        else:
            frac = 0.0
        phases.append((cells[0], status.split("(")[0], frac))
    if not phases:
        return None, []
    return sum(f for _, _, f in phases) / len(phases), phases

def bar(frac):
    filled = round(frac * BAR_WIDTH)
    return "[" + "#" * filled + "-" * (BAR_WIDTH - filled) + f"] {round(frac*100):3d}%"

def gate_pressure(root):
    gates = root / "GATES.md"
    out = []
    if not gates.exists():
        return out
    now = datetime.now()
    for cells in parse_rows(gates.read_text(encoding="utf-8"), "G-"):
        if len(cells) >= 5 and cells[4].upper().startswith("OPEN"):
            try:
                age_h = (now - datetime.strptime(cells[3], "%Y-%m-%d")).total_seconds() / 3600
            except ValueError:
                age_h = -1
            flag = "!! SLA BREACH" if age_h > 48 else f"{int(max(age_h,0))}h on the clock"
            out.append(f"  {cells[0]}  OPEN  {flag}  -- {cells[1][:58]}")
    return out

def last_checkpoint(root):
    try:
        r = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%h %ad %s", "--date=short"],
                           capture_output=True, text=True)
        return r.stdout.strip() or "(no commits yet -- gate G-001)"
    except OSError:
        return "(git unavailable)"


def receipt_progress(root):
    directory = root / "workflow" / "receipts"
    counts = {"verified_loops": 0, "infrastructure": 0, "invalidated": 0, "other": 0}
    if not directory.exists():
        return counts
    for path in directory.glob("*.md"):
        fields = {}
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            match = re.match(r"^([A-Z][A-Z0-9_]*):\s*(.*)$", line)
            if match:
                fields[match.group(1)] = match.group(2).strip().upper()
        state = fields.get("STATE", "")
        kind = fields.get("PROGRESS", "")
        if state == "INVALIDATED":
            counts["invalidated"] += 1
        elif state == "DONE" and kind in {"DECISION", "MEASUREMENT"}:
            counts["verified_loops"] += 1
        elif state == "DONE" and kind == "INFRASTRUCTURE":
            counts["infrastructure"] += 1
        else:
            counts["other"] += 1
    return counts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    args = ap.parse_args()
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent

    overall, phases = phase_progress(root)
    print("SEED STATUS -- " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    print()
    if overall is None:
        print("  no parseable Phasing table in workflow/PLAN.md")
    else:
        print("  overall  " + bar(overall))
        for name, status, frac in phases:
            print(f"  {name:<24} {bar(frac)}  {status}")
    print()
    open_gates = gate_pressure(root)
    print("  gates:" if open_gates else "  gates: none open")
    for g in open_gates:
        print(g)
    progress = receipt_progress(root)
    receipts = sum(progress.values())
    print(f"  receipts banked: {receipts}")
    print(
        "  verified progress: "
        f"{progress['verified_loops']} decision/measurement loop(s); "
        f"{progress['infrastructure']} infrastructure completion(s); "
        f"{progress['invalidated']} invalidated"
    )
    print(f"  last checkpoint: {last_checkpoint(root)}")

if __name__ == "__main__":
    main()
