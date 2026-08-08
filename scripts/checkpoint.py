#!/usr/bin/env python3
"""checkpoint.py -- verified snapshots. Git is the checkpoint store ("the repo IS the memory").

A checkpoint is a git commit that onboard_check has passed. Red checks = no checkpoint; a
snapshot of a lying repo preserves the lie. With --full, the sabotage test must also pass
(use before transplant, release, or any handoff to another machine).

Usage:  python scripts/checkpoint.py "label for this checkpoint" [--full]
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("label", help="short description of this checkpoint")
    ap.add_argument("--full", action="store_true", help="also require sabotage_test green")
    args = ap.parse_args()

    checks = [("onboard_check", [sys.executable, "scripts/onboard_check.py"])]
    if args.full:
        checks.append(("sabotage_test", [sys.executable, "scripts/sabotage_test.py"]))
    for name, cmd in checks:
        r = run(cmd)
        if r.returncode != 0:
            print(r.stdout)
            print(f"REFUSED: {name} is red. No checkpoint of a lying repo -- fix it first.")
            return 1
        print(f"verified  {name} green")

    run(["git", "add", "-A"])
    r = run(["git", "commit", "-m", f"checkpoint: {args.label} [verified"
             + (", sabotage-tested]" if args.full else "]")])
    if r.returncode != 0:
        if "nothing to commit" in (r.stdout + r.stderr):
            print("nothing to commit -- working tree already checkpointed")
            return 0
        print(r.stdout + r.stderr)
        return 1
    print(run(["git", "log", "-1", "--format=checkpoint %h  %s"]).stdout.strip())
    return 0

if __name__ == "__main__":
    sys.exit(main())
