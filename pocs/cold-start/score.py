#!/usr/bin/env python3
"""Machine-score a cold-start comprehension record against a frozen truth contract."""

import argparse
import json
import sys
from pathlib import Path


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON from {path}: {exc}") from exc


def score(contract, answer):
    expected = contract["required"]
    observed = answer.get("answers", {})
    fields = {}
    for name, wanted in expected.items():
        got = observed.get(name)
        fields[name] = {"expected": wanted, "observed": got, "correct": got == wanted}

    elapsed = answer.get("elapsed_seconds")
    elapsed_valid = isinstance(elapsed, (int, float)) and not isinstance(elapsed, bool) and elapsed >= 0
    within_time = elapsed_valid and elapsed <= contract["time_limit_seconds"]
    identity_ok = answer.get("target_commit") == contract["target_commit"]
    all_facts = all(item["correct"] for item in fields.values())
    passed = identity_ok and within_time and all_facts
    return {
        "contract_version": contract["contract_version"],
        "target_project": contract["target_project"],
        "passed": passed,
        "identity_ok": identity_ok,
        "within_time": within_time,
        "elapsed_seconds": elapsed,
        "time_limit_seconds": contract["time_limit_seconds"],
        "facts_correct": sum(item["correct"] for item in fields.values()),
        "facts_total": len(fields),
        "fields": fields,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("answer", help="JSON record produced after cold onboarding")
    parser.add_argument(
        "--contract",
        default=str(Path(__file__).with_name("contract.json")),
        help="frozen truth contract",
    )
    args = parser.parse_args()
    try:
        result = score(load_json(args.contract), load_json(args.answer))
    except (ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
