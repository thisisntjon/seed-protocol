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
import re
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "onboard_check.py"
SCHEMA_CHECK = ROOT / "scripts" / "schema_check.py"
STATUS = ROOT / "scripts" / "status.py"
TRANSPLANT = ROOT / "scripts" / "transplant.py"


def run_check(root):
    result = subprocess.run(
        [sys.executable, str(CHECK), "--root", str(root)],
        capture_output=True,
        text=True,
    )
    return result.returncode


def run_schema_check(root):
    result = subprocess.run(
        [sys.executable, str(SCHEMA_CHECK), "--root", str(root)],
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


def progress_counts(output):
    match = re.search(
        r"verified progress: (\d+) decision/measurement loop\(s\); "
        r"(\d+) infrastructure completion\(s\); (\d+) invalidated",
        output,
    )
    return tuple(int(value) for value in match.groups()) if match else None


def fresh_copy(tmp, name):
    destination = Path(tmp) / name
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    return destination


def init_target(path):
    path.mkdir(parents=True)
    result = subprocess.run(
        ["git", "init", "-b", "main", str(path)],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def run_transplant(target, apply=False, upgrade=False):
    command = [sys.executable, str(TRANSPLANT), "--target", str(target)]
    if apply:
        command.append("--apply")
    if upgrade:
        command.append("--upgrade")
    return subprocess.run(command, capture_output=True, text=True)


def add_gate(root, row):
    path = root / "GATES.md"
    path.write_text(path.read_text(encoding="utf-8") + "\n" + row + "\n", encoding="utf-8")


def require_git_clone():
    """The transplant cases read SEED's own git identity; a ZIP download has none."""
    probe = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True
    )
    if not (ROOT / ".git").exists() or probe.returncode != 0:
        print(
            "sabotage_test requires a git clone (uses git history); "
            "download ZIP is not supported"
        )
        return False
    return True


def main():
    if not require_git_clone():
        return 2
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        clean = fresh_copy(tmp, "clean")
        results.append(("clean repo passes", run_check(clean) == 0))
        results.append(("clean repo passes schema check", run_schema_check(clean) == 0))
        status_code, status_output = run_status(clean)
        baseline_counts = progress_counts(status_output)

        infrastructure = fresh_copy(tmp, "infrastructure-progress")
        (infrastructure / "workflow" / "receipts" / "2026-08-08-infrastructure.md").write_text(
            "STATE: DONE\nOBJECT: infrastructure work\nEXACT_REF: abc123\nEVIDENCE: command passed\n"
            "PROGRESS: INFRASTRUCTURE\nEFFECT: none - infrastructure\n"
            "BLOCKED_ON: none\nNEXT_OWNER: none\n",
            encoding="utf-8",
        )
        infra_code, infra_output = run_status(infrastructure)
        infra_counts = progress_counts(infra_output)
        results.append(
            (
                "infrastructure does not count as verified progress",
                status_code == 0
                and infra_code == 0
                and baseline_counts is not None
                and infra_counts
                == (baseline_counts[0], baseline_counts[1] + 1, baseline_counts[2]),
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
        measured_counts = progress_counts(status_output)
        results.append(
            (
                "measured loop increments verified progress",
                status_code == 0
                and baseline_counts is not None
                and measured_counts
                == (baseline_counts[0] + 1, baseline_counts[1], baseline_counts[2]),
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
        ledger = retracted / "workflow" / "canon" / "RETRACTIONS.md"
        ledger.write_text(
            ledger.read_text(encoding="utf-8")
            + "\n| SABOTAGE-RETRACTED-TOKEN | replacement | seeded test token | 2026-08-08 |\n",
            encoding="utf-8",
        )
        docs = retracted / "docs" / "nested"
        docs.mkdir(parents=True)
        (docs / "notes.md").write_text(
            "The obsolete value was SABOTAGE-RETRACTED-TOKEN.\n",
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

        schema_bad_state = fresh_copy(tmp, "schema-bad-receipt-state")
        (schema_bad_state / "workflow" / "receipts" / "2026-09-02-hopeful.md").write_text(
            "STATE: HOPEFUL\nOBJECT: something\nEXACT_REF: abc123\nEVIDENCE: command passed\n"
            "PROGRESS: INFRASTRUCTURE\nEFFECT: none - infrastructure\nSESSION_ID: sabotage\n"
            "NEXT_OWNER: none\n",
            encoding="utf-8",
        )
        results.append(("schema rejects invalid receipt STATE token", run_schema_check(schema_bad_state) != 0))

        schema_free_outcome = fresh_copy(tmp, "schema-free-text-outcome")
        experiments = schema_free_outcome / "workflow" / "experiments"
        experiments.mkdir(parents=True, exist_ok=True)
        (experiments / "2026-09-02-narrative.md").write_text(
            "HYPOTHESIS: x\nOBJECT: abc123\nDEPLOYED_FORM: local\nMEASUREMENT: n=1\n"
            "PASS_BAR: 1\nKILL_BAR: 0\nCOST: none\n"
            "OUTCOME: looks promising, basically a pass\n"
            "INDEPENDENT_REPRO: pending\n",
            encoding="utf-8",
        )
        results.append(("schema rejects free-text experiment OUTCOME", run_schema_check(schema_free_outcome) != 0))

        schema_missing_field = fresh_copy(tmp, "schema-missing-field")
        (schema_missing_field / "workflow" / "receipts" / "2026-09-02-no-owner.md").write_text(
            "STATE: DONE\nOBJECT: something\nEXACT_REF: abc123\nEVIDENCE: command passed\n"
            "PROGRESS: INFRASTRUCTURE\nEFFECT: none - infrastructure\nSESSION_ID: sabotage\n",
            encoding="utf-8",
        )
        results.append(("schema rejects receipt missing NEXT_OWNER", run_schema_check(schema_missing_field) != 0))

        schema_drift = fresh_copy(tmp, "schema-vocabulary-drift")
        kernel = schema_drift / "schema" / "evidence-kernel.schema.json"
        kernel.write_text(
            kernel.read_text(encoding="utf-8").replace('"INVALIDATED"', '"VIBES"'),
            encoding="utf-8",
        )
        results.append(("schema vocabulary drift from checker fails", run_schema_check(schema_drift) != 0))

        dry_target = Path(tmp) / "transplant-dry-target"
        initialized = init_target(dry_target)
        dry_result = run_transplant(dry_target)
        results.append(
            (
                "transplant dry-run writes nothing",
                initialized and dry_result.returncode == 0 and not (dry_target / "LAWS.md").exists(),
            )
        )

        apply_target = Path(tmp) / "transplant-apply-target"
        initialized = init_target(apply_target)
        apply_result = run_transplant(apply_target, apply=True)
        provenance_path = apply_target / "workflow" / "SEED-TRANSPLANT.json"
        provenance = json.loads(provenance_path.read_text(encoding="utf-8")) if provenance_path.exists() else {}
        results.append(
            (
                "transplant copies portable core with provenance",
                initialized
                and apply_result.returncode == 0
                and (apply_target / "LAWS.md").exists()
                and provenance_path.exists()
                and len(provenance.get("portable_identity_sha256", "")) == 64,
            )
        )

        conflict_target = Path(tmp) / "transplant-conflict-target"
        initialized = init_target(conflict_target)
        first_result = run_transplant(conflict_target, apply=True)
        laws = conflict_target / "LAWS.md"
        laws.write_text("target-owned content\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(conflict_target), "add", "-A"], capture_output=True)
        subprocess.run(
            [
                "git", "-C", str(conflict_target), "-c", "user.name=Test", "-c",
                "user.email=test@local", "commit", "-m", "target state",
            ],
            capture_output=True,
        )
        conflict_result = run_transplant(conflict_target, apply=True)
        results.append(
            (
                "transplant refuses and preserves differing target files",
                initialized
                and first_result.returncode == 0
                and conflict_result.returncode != 0
                and laws.read_text(encoding="utf-8") == "target-owned content\n",
            )
        )

        upgrade_target = Path(tmp) / "transplant-upgrade-target"
        initialized = init_target(upgrade_target)
        first_result = run_transplant(upgrade_target, apply=True)
        laws = upgrade_target / "LAWS.md"
        old_content = "managed old version\n"
        laws.write_text(old_content, encoding="utf-8")
        old_hash = hashlib.sha256(laws.read_bytes()).hexdigest()
        provenance_path = upgrade_target / "workflow" / "SEED-TRANSPLANT.json"
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        for item in provenance["portable_files"]:
            if item["path"] == "LAWS.md":
                item["sha256"] = old_hash
        provenance_path.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(upgrade_target), "add", "-A"], capture_output=True)
        subprocess.run(
            [
                "git", "-C", str(upgrade_target), "-c", "user.name=Test", "-c",
                "user.email=test@local", "commit", "-m", "old managed core",
            ],
            capture_output=True,
        )
        upgrade_result = run_transplant(upgrade_target, apply=True, upgrade=True)
        upgrade_ok = (
            initialized
            and first_result.returncode == 0
            and upgrade_result.returncode == 0
            and laws.read_bytes() == (ROOT / "LAWS.md").read_bytes()
        )
        if not upgrade_ok:
            print("DETAIL  managed-upgrade stdout:", upgrade_result.stdout.strip())
            print("DETAIL  managed-upgrade stderr:", upgrade_result.stderr.strip())
        results.append(
            (
                "managed upgrade replaces only provenance-matched bytes",
                upgrade_ok,
            )
        )

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
