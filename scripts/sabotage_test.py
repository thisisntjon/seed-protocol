#!/usr/bin/env python3
"""Prove that onboard_check fails on each defect class it claims to detect.

Every case runs in a disposable copy. A green clean copy plus red sabotaged copies is the
minimum evidence that the guard has refutation power; it is not evidence that every possible
defect is covered.
"""
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "onboard_check.py"
STATUS = ROOT / "scripts" / "status.py"


def run_check(root):
    result = subprocess.run(
        [sys.executable, str(CHECK), "--root", str(root)],
        capture_output=True,
        text=True,
    )
    return result.returncode


def run_status(root):
    result = subprocess.run(
        [sys.executable, str(STATUS), "--root", str(root)],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout


def fresh_copy(tmp, name):
    destination = Path(tmp) / name
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    return destination


def add_gate(root, row):
    path = root / "GATES.md"
    path.write_text(path.read_text(encoding="utf-8") + "\n" + row + "\n", encoding="utf-8")


def main():
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        clean = fresh_copy(tmp, "clean")
        results.append(("clean repo passes", run_check(clean) == 0))
        status_code, status_output = run_status(clean)
        results.append(
            (
                "infrastructure does not count as verified progress",
                status_code == 0
                and "0 decision/measurement loop(s); 1 infrastructure completion(s); 1 invalidated"
                in status_output,
            )
        )

        measured = fresh_copy(tmp, "measured-progress")
        (measured / "workflow" / "receipts" / "2026-08-08-measurement.md").write_text(
            "STATE: DONE\nOBJECT: measured loop\nEXACT_REF: abc123\nEVIDENCE: result.json\n"
            "PROGRESS: MEASUREMENT\nEFFECT: onboarding time measured at 12 minutes\n"
            "BLOCKED_ON: none\nNEXT_OWNER: none\n",
            encoding="utf-8",
        )
        status_code, status_output = run_status(measured)
        results.append(
            (
                "measured loop increments verified progress",
                status_code == 0
                and "1 decision/measurement loop(s); 1 infrastructure completion(s); 1 invalidated"
                in status_output,
            )
        )

        missing_path = fresh_copy(tmp, "missing-path")
        (missing_path / "LAWS.md").unlink()
        results.append(("missing claimed path fails", run_check(missing_path) != 0))

        stale_gate = fresh_copy(tmp, "stale-gate")
        old = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        add_gate(stale_gate, f"| G-SABOTAGE-STALE | test overdue gate | human | {old} | OPEN |")
        results.append(("independent overdue gate fails", run_check(stale_gate) != 0))

        invalid_gate = fresh_copy(tmp, "invalid-gate")
        today = datetime.now().strftime("%Y-%m-%d")
        add_gate(invalid_gate, f"| G-SABOTAGE-STATUS | test bad status | human | {today} | MAYBE |")
        results.append(("invalid gate status fails", run_check(invalid_gate) != 0))

        bad_receipt = fresh_copy(tmp, "bad-receipt")
        (bad_receipt / "workflow" / "receipts" / "2026-08-08-bad.md").write_text(
            "STATE: DONE\nOBJECT: something\nEXACT_REF: abc123\nPROGRESS: INFRASTRUCTURE\n"
            "EFFECT: none - infrastructure\nNEXT_OWNER: none\n",
            encoding="utf-8",
        )
        results.append(("receipt without evidence fails", run_check(bad_receipt) != 0))

        bad_state = fresh_copy(tmp, "bad-receipt-state")
        (bad_state / "workflow" / "receipts" / "2026-08-08-wishful.md").write_text(
            "STATE: WISHFUL\nOBJECT: something\nEXACT_REF: abc123\n"
            "EVIDENCE: none\nPROGRESS: INFRASTRUCTURE\nEFFECT: none - infrastructure\n"
            "NEXT_OWNER: none\n",
            encoding="utf-8",
        )
        results.append(("invalid receipt state fails", run_check(bad_state) != 0))

        missing_progress = fresh_copy(tmp, "missing-progress")
        (missing_progress / "workflow" / "receipts" / "2026-08-08-no-progress.md").write_text(
            "STATE: DONE\nOBJECT: something\nEXACT_REF: abc123\nEVIDENCE: command passed\n"
            "EFFECT: none - not classified\nNEXT_OWNER: none\n",
            encoding="utf-8",
        )
        results.append(("completed receipt without progress class fails", run_check(missing_progress) != 0))

        retracted = fresh_copy(tmp, "nested-retraction")
        docs = retracted / "docs" / "nested"
        docs.mkdir(parents=True)
        (docs / "notes.md").write_text(
            "The obsolete score was EXAMPLE-999.9.\n",
            encoding="utf-8",
        )
        results.append(("retracted token in nested docs fails", run_check(retracted) != 0))

        bad_dispatch = fresh_copy(tmp, "bad-dispatch")
        dispatches = bad_dispatch / "workflow" / "dispatches"
        dispatches.mkdir(parents=True, exist_ok=True)
        (dispatches / "bad.md").write_text(
            "TO: worker\nOBJECT: thing\nEXACT_REF: abc123\nACTION: build\n"
            "FENCES: none\nNEXT_EVENT: verify\n",
            encoding="utf-8",
        )
        results.append(("dispatch without acceptance fails", run_check(bad_dispatch) != 0))

        bad_experiment = fresh_copy(tmp, "bad-experiment")
        experiments = bad_experiment / "workflow" / "experiments"
        experiments.mkdir(parents=True, exist_ok=True)
        (experiments / "bad.md").write_text(
            "HYPOTHESIS: x\nOBJECT: abc123\nDEPLOYED_FORM: local\nMEASUREMENT: n=1\n"
            "PASS_BAR: 1\nKILL_BAR: 0\nCOST: none\nOUTCOME: CELEBRATE\n"
            "INDEPENDENT_REPRO: pending\n",
            encoding="utf-8",
        )
        results.append(("invalid experiment outcome fails", run_check(bad_experiment) != 0))

        bad_handoff = fresh_copy(tmp, "bad-handoff")
        (bad_handoff / "workflow" / "handoffs" / "bad.md").write_text(
            "# We are probably done\n",
            encoding="utf-8",
        )
        results.append(("malformed handoff fails", run_check(bad_handoff) != 0))

        unsupported_claim = fresh_copy(tmp, "unsupported-claim")
        claims = unsupported_claim / "CLAIMS.md"
        claims.write_text(
            claims.read_text(encoding="utf-8")
            + "\n| C-SABOTAGE | This is definitely proven. | SUPPORTED | A test could fail. | none |\n",
            encoding="utf-8",
        )
        results.append(("supported claim without bound evidence fails", run_check(unsupported_claim) != 0))

    ok = True
    for name, passed in results:
        print(("PASS    " if passed else "FAIL    ") + name)
        ok = ok and passed
    count = sum(1 for _, passed in results if passed)
    print(
        f"\nSABOTAGE TEST {count}/{len(results)} "
        + ("PASSED -- every seeded defect was detected" if ok else "FAILED -- the guard is decorative, do not trust green")
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
