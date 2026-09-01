#!/usr/bin/env python3
"""Cold-start orientation. Never act on remembered state.

Prints SHA, START-HERE four lines, plan stage, open gates, newest handoff, next action.
Exit 2 if the substrate is missing. ASCII only.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


def find_root(explicit: Path | None) -> Path:
    if explicit:
        root = explicit.resolve()
        if not (root / "START-HERE.md").exists():
            raise SystemExit("REFUSED: START-HERE.md missing at --root")
        return root
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "START-HERE.md").exists():
            return candidate
    raise SystemExit("REFUSED: START-HERE.md not found (never act on remembered state)")


def git_sha(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return "(no git HEAD)"
    return result.stdout.strip() or "(no git HEAD)"


def four_lines(root: Path) -> list[str]:
    text = (root / "START-HERE.md").read_text(encoding="utf-8")
    match = re.search(r"## THE WHOLE JOB[^\n]*\n+```[^\n]*\n(.*?)```", text, re.S)
    if not match:
        raise SystemExit("REFUSED: START-HERE.md has no four-line job block")
    lines = [ln.rstrip() for ln in match.group(1).splitlines() if ln.strip()]
    return lines[:8]


def stage_line(path: Path) -> str | None:
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lower().startswith("current stage:"):
            return line.strip()
    return None


def open_gates(root: Path) -> list[str]:
    path = root / "GATES.md"
    if not path.exists():
        return ["GATES.md missing"]
    out = []
    now = datetime.now()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not cells[0].startswith("G-"):
            continue
        status = cells[4].upper()
        if status != "OPEN":
            continue
        try:
            opened = datetime.strptime(cells[3], "%Y-%m-%d")
            age_h = (now - opened).total_seconds() / 3600
            flag = "SLA BREACH" if age_h > 48 else f"{int(max(age_h, 0))}h"
        except ValueError:
            flag = "bad-date"
        out.append(f"{cells[0]} {flag} -- {cells[1][:70]}")
    return out


def newest_handoff(root: Path) -> str:
    folder = root / "workflow" / "handoffs"
    if not folder.exists():
        return "(none)"
    files = [p for p in folder.glob("*.md") if p.is_file()]
    if not files:
        return "(none)"
    newest = max(files, key=lambda p: p.stat().st_mtime)
    return newest.name


def next_action(root: Path) -> str:
    for rel in (
        "workflow/blueprint/PLAN.md",
        "workflow/harvest/PLAN.md",
        "workflow/PLAN.md",
    ):
        stage = stage_line(root / rel)
        if stage:
            return f"{rel}: {stage}"
    return "no Current stage: line found — write one before acting"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args(argv)
    try:
        root = find_root(args.root)
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print("FACTORY ORIENT -- " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("root  " + str(root))
    print("sha   " + git_sha(root))
    print()
    print("THE WHOLE JOB")
    for line in four_lines(root):
        print("  " + line)
    print()
    print("plans")
    for rel in (
        "workflow/blueprint/PLAN.md",
        "workflow/harvest/PLAN.md",
        "workflow/PLAN.md",
    ):
        stage = stage_line(root / rel)
        print("  " + rel + ": " + (stage or "(missing or no Current stage)"))
    print()
    gates = open_gates(root)
    print("open gates: " + ("none" if not gates else ""))
    for row in gates:
        print("  " + row)
    print("newest handoff: " + newest_handoff(root))
    print()
    print("NEXT: " + next_action(root))
    print("do not act on remembered state")
    return 0


if __name__ == "__main__":
    sys.exit(main())
