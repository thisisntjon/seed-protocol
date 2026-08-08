#!/usr/bin/env python3
"""sabotage_test.py -- Law 2 applied to our own guard.

A guard is not trusted until it fails on the defect it claims to catch. This seeds four defect
classes into throwaway copies of the repo and requires onboard_check.py to go red on each,
and green on the clean copy. If any sabotage stays green, the checker is decorative.
"""
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "onboard_check.py"

def run_check(root):
    r = subprocess.run([sys.executable, str(CHECK), "--root", str(root)],
                       capture_output=True, text=True)
    return r.returncode

def fresh_copy(tmp, name):
    dst = Path(tmp) / name
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    return dst

def main():
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        clean = fresh_copy(tmp, "clean")
        results.append(("clean repo passes", run_check(clean) == 0))

        s1 = fresh_copy(tmp, "s1-missing-path")
        (s1 / "LAWS.md").unlink()
        results.append(("missing claimed path fails", run_check(s1) != 0))

        s2 = fresh_copy(tmp, "s2-stale-gate")
        gates = s2 / "GATES.md"
        old = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        body = gates.read_text(encoding="utf-8")
        import re
        body = re.sub(r"\| (\d{4}-\d{2}-\d{2}) \| OPEN \|", f"| {old} | OPEN |", body)
        gates.write_text(body, encoding="utf-8")
        results.append(("gate past SLA fails", run_check(s2) != 0))

        s3 = fresh_copy(tmp, "s3-bad-receipt")
        (s3 / "workflow" / "receipts" / "2026-08-08-bad.md").write_text(
            "STATE: DONE\nOBJECT: something\nNEXT_OWNER: none\n", encoding="utf-8")
        results.append(("receipt without EVIDENCE fails", run_check(s3) != 0))

        s4 = fresh_copy(tmp, "s4-retracted-cite")
        (s4 / "workflow" / "handoffs" / "2026-08-08-notes.md").write_text(
            "The score was EXAMPLE-999.9 at last reading.\n", encoding="utf-8")
        results.append(("retracted token cited fails", run_check(s4) != 0))

    ok = True
    for name, passed in results:
        print(("PASS    " if passed else "FAIL    ") + name)
        ok = ok and passed
    print("\nSABOTAGE TEST " + ("PASSED -- the guard demonstrably catches its defects"
                                if ok else "FAILED -- the guard is decorative, do not trust green"))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
