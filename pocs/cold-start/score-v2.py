#!/usr/bin/env python3
"""Score declared semantic choices plus per-fact evidence against a frozen v2 rubric."""

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
    observed = answer.get("answers", {})
    submitted_evidence = answer.get("evidence", {})
    known_sources = contract["sources"]
    fields = {}
    for name, rule in contract["rubric"].items():
        got = observed.get(name)
        cited = submitted_evidence.get(name, [])
        if not isinstance(cited, list):
            cited = []
        matched_evidence = sorted(
            set(cited) & set(rule["evidence_any"]) & set(known_sources)
        )
        fields[name] = {
            "allowed_value": got in rule["allowed"],
            "correct": got == rule["expected"],
            "evidence_ok": bool(matched_evidence),
            "evidence": matched_evidence,
            "evidence_blob_oids": {path: known_sources[path] for path in matched_evidence},
            "observed": got,
        }

    elapsed = answer.get("elapsed_seconds")
    elapsed_valid = isinstance(elapsed, (int, float)) and not isinstance(elapsed, bool) and elapsed >= 0
    within_time = elapsed_valid and elapsed <= contract["time_limit_seconds"]
    identity_ok = answer.get("target_commit") == contract["target_commit"]
    facts_ok = all(item["allowed_value"] and item["correct"] for item in fields.values())
    evidence_ok = all(item["evidence_ok"] for item in fields.values())
    passed = identity_ok and within_time and facts_ok and evidence_ok
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
        "evidence_correct": sum(item["evidence_ok"] for item in fields.values()),
        "evidence_total": len(fields),
        "fields": fields,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("answer", help="JSON record produced after cold onboarding")
    parser.add_argument("--contract", default=str(Path(__file__).with_name("contract-v2.json")))
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
