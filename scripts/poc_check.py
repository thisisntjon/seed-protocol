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

    print("POC CHECK PASSED: 10/10 controls behaved as predeclared")
    return 0


if __name__ == "__main__":
    sys.exit(main())
