#!/usr/bin/env python3
"""Calibrate Bonkers POCs, including expected-red controls."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run(*parts):
    return subprocess.run(
        [sys.executable, *map(str, parts)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def check(name, condition, detail):
    if not condition:
        raise AssertionError(f"{name}: {detail}")
    print(f"PASS  {name}")


def run_command(parts, cwd):
    return subprocess.run(parts, cwd=cwd, capture_output=True, text=True)


def main():
    registry = json.loads((ROOT / "pocs" / "POC-REGISTRY.json").read_text(encoding="utf-8"))
    pocs = registry["pocs"]
    ids = [item["id"] for item in pocs]
    registry_ok = (
        len(pocs) == 10
        and len(set(ids)) == 10
        and ids == [f"POC-{number:02d}" for number in range(1, 11)]
        and all(item["status"] in registry["status_vocabulary"] for item in pocs)
        and all(0 <= item["progress_percent"] <= 100 for item in pocs)
        and all((ROOT / item["evidence"]).exists() for item in pocs)
    )
    check("ten-POC registry is complete and evidence-bound", registry_ok, json.dumps(registry, indent=2))

    cold = ROOT / "pocs" / "cold-start"
    valid = run(cold / "score.py", cold / "example-valid.json")
    check("cold-start valid control", valid.returncode == 0, valid.stdout + valid.stderr)
    check("cold-start valid JSON", json.loads(valid.stdout)["passed"] is True, valid.stdout)

    invalid = run(cold / "score.py", cold / "example-invalid.json")
    check("cold-start false-confidence control", invalid.returncode == 1, invalid.stdout + invalid.stderr)
    invalid_record = json.loads(invalid.stdout)
    check(
        "cold-start rejects false confidence",
        invalid_record["passed"] is False and invalid_record["facts_correct"] < invalid_record["facts_total"],
        invalid.stdout,
    )

    valid_payload = json.loads((cold / "example-valid.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as temp_dir:
        stale_path = Path(temp_dir) / "stale.json"
        stale_payload = dict(valid_payload)
        stale_payload["target_commit"] = "0" * 40
        stale_path.write_text(json.dumps(stale_payload), encoding="utf-8")
        stale = run(cold / "score.py", stale_path)
        check("cold-start rejects stale identity", stale.returncode == 1, stale.stdout + stale.stderr)

        overtime_path = Path(temp_dir) / "overtime.json"
        overtime_payload = dict(valid_payload)
        overtime_payload["elapsed_seconds"] = 901
        overtime_path.write_text(json.dumps(overtime_payload), encoding="utf-8")
        overtime = run(cold / "score.py", overtime_path)
        check("cold-start enforces time ceiling", overtime.returncode == 1, overtime.stdout + overtime.stderr)

    valid_v2 = run(cold / "score-v2.py", cold / "example-valid-v2.json")
    valid_v2_record = json.loads(valid_v2.stdout)
    check(
        "cold-start v2 declared rubric passes",
        valid_v2.returncode == 0
        and valid_v2_record["facts_correct"] == 8
        and valid_v2_record["evidence_correct"] == 8,
        valid_v2.stdout + valid_v2.stderr,
    )

    invalid_v2 = run(cold / "score-v2.py", cold / "example-invalid-v2.json")
    check("cold-start v2 rejects wrong choices", invalid_v2.returncode == 1, invalid_v2.stdout + invalid_v2.stderr)

    with tempfile.TemporaryDirectory() as temp_dir:
        v2_payload = json.loads((cold / "example-valid-v2.json").read_text(encoding="utf-8"))
        missing_evidence_path = Path(temp_dir) / "missing-evidence.json"
        v2_payload["evidence"]["causal_benefit"] = []
        missing_evidence_path.write_text(json.dumps(v2_payload), encoding="utf-8")
        missing_evidence = run(cold / "score-v2.py", missing_evidence_path)
        check(
            "cold-start v2 requires per-fact evidence",
            missing_evidence.returncode == 1,
            missing_evidence.stdout + missing_evidence.stderr,
        )

        unknown_value_path = Path(temp_dir) / "unknown-value.json"
        v2_payload = json.loads((cold / "example-valid-v2.json").read_text(encoding="utf-8"))
        v2_payload["answers"]["current_phase"] = "FOUNDATION_VALIDATION"
        unknown_value_path.write_text(json.dumps(v2_payload), encoding="utf-8")
        unknown_value = run(cold / "score-v2.py", unknown_value_path)
        check(
            "cold-start v2 rejects undeclared vocabulary",
            unknown_value.returncode == 1,
            unknown_value.stdout + unknown_value.stderr,
        )

    with tempfile.TemporaryDirectory() as temp_dir:
        fixture_repo = Path(temp_dir) / "fixture-repo"
        fixture_repo.mkdir()
        for command in (
            ["git", "init", "--quiet"],
            ["git", "config", "user.name", "POC Fixture"],
            ["git", "config", "user.email", "poc@example.invalid"],
        ):
            result = run_command(command, fixture_repo)
            check("cold-start v3 fixture setup", result.returncode == 0, result.stdout + result.stderr)
        (fixture_repo / "state.md").write_text("| P1 Foundation | ACTIVE |\n", encoding="utf-8")
        (fixture_repo / "irrelevant.md").write_text("Nothing about the current phase.\n", encoding="utf-8")
        result = run_command(["git", "add", "."], fixture_repo)
        check("cold-start v3 fixture add", result.returncode == 0, result.stdout + result.stderr)
        result = run_command(["git", "commit", "--quiet", "-m", "fixture"], fixture_repo)
        check("cold-start v3 fixture commit", result.returncode == 0, result.stdout + result.stderr)
        commit = run_command(["git", "rev-parse", "HEAD"], fixture_repo).stdout.strip()

        fixture_contract = {
            "contract_version": 3,
            "target_project": "fixture",
            "target_commit": commit,
            "time_limit_seconds": 900,
            "rubric": {
                "current_phase": {
                    "allowed": ["P1_FOUNDATION", "P2_PILOT"],
                    "expected": "P1_FOUNDATION",
                    "evidence_anchor_any": [[r"P1\s+Foundation", "ACTIVE"]],
                }
            },
        }
        fixture_answer = {
            "target_commit": commit,
            "elapsed_seconds": 60,
            "answers": {"current_phase": "P1_FOUNDATION"},
            "evidence": {"current_phase": ["state.md"]},
        }
        contract_path = Path(temp_dir) / "contract.json"
        answer_path = Path(temp_dir) / "answer.json"
        contract_path.write_text(json.dumps(fixture_contract), encoding="utf-8")
        answer_path.write_text(json.dumps(fixture_answer), encoding="utf-8")

        valid_v3 = run(
            cold / "score-v3.py",
            answer_path,
            "--target-repo",
            fixture_repo,
            "--contract",
            contract_path,
        )
        check("cold-start v3 validates committed evidence content", valid_v3.returncode == 0, valid_v3.stdout + valid_v3.stderr)

        fixture_answer["evidence"]["current_phase"] = ["irrelevant.md"]
        answer_path.write_text(json.dumps(fixture_answer), encoding="utf-8")
        irrelevant_v3 = run(
            cold / "score-v3.py",
            answer_path,
            "--target-repo",
            fixture_repo,
            "--contract",
            contract_path,
        )
        check("cold-start v3 rejects irrelevant evidence", irrelevant_v3.returncode == 1, irrelevant_v3.stdout + irrelevant_v3.stderr)

        fixture_answer["evidence"]["current_phase"] = ["../state.md"]
        answer_path.write_text(json.dumps(fixture_answer), encoding="utf-8")
        traversal_v3 = run(
            cold / "score-v3.py",
            answer_path,
            "--target-repo",
            fixture_repo,
            "--contract",
            contract_path,
        )
        check("cold-start v3 rejects path traversal", traversal_v3.returncode == 1, traversal_v3.stdout + traversal_v3.stderr)

    trap = ROOT / "pocs" / "deceptive-green"
    weak = run(trap / "weak_check.py")
    check("deceptive-green weak evaluator is green", weak.returncode == 0, weak.stdout + weak.stderr)

    protected = run(trap / "artifact_check.py")
    check("deceptive-green protected evaluator turns red", protected.returncode != 0, protected.stdout + protected.stderr)
    check(
        "deceptive-green explains mismatch",
        "deployed artifact mismatch" in (protected.stdout + protected.stderr),
        protected.stdout + protected.stderr,
    )

    print("POC CHECK PASSED: 22/22 controls behaved as predeclared")
    return 0


if __name__ == "__main__":
    sys.exit(main())
