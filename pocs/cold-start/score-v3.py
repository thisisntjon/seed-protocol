#!/usr/bin/env python3
"""Score declared facts and validate cited evidence from the exact target git commit."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON from {path}: {exc}") from exc


def safe_relative_path(raw):
    if not isinstance(raw, str) or not raw.strip():
        return None
    normalized = raw.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts or ".git" in path.parts:
        return None
    return str(path)


def git_text(repo, commit, path):
    proc = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.stdout if proc.returncode == 0 else None


def matching_anchor(text, clauses):
    for index, patterns in enumerate(clauses):
        if all(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) for pattern in patterns):
            return index
    return None


def score(contract, answer, target_repo):
    commit = contract["target_commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("contract target_commit must be a full lowercase git object id")
    commit_check = subprocess.run(
        ["git", "-C", str(target_repo), "cat-file", "-e", f"{commit}^{{commit}}"],
        capture_output=True,
        text=True,
    )
    source_commit_ok = commit_check.returncode == 0

    observed = answer.get("answers", {})
    submitted_evidence = answer.get("evidence", {})
    fields = {}
    for name, rule in contract["rubric"].items():
        got = observed.get(name)
        cited = submitted_evidence.get(name, [])
        if not isinstance(cited, list):
            cited = []
        evidence_results = []
        for raw_path in cited:
            path = safe_relative_path(raw_path)
            text = git_text(target_repo, commit, path) if source_commit_ok and path else None
            anchor_index = matching_anchor(text, rule["evidence_anchor_any"]) if text is not None else None
            evidence_results.append(
                {
                    "submitted": raw_path,
                    "path": path,
                    "exists_at_commit": text is not None,
                    "matched_anchor": anchor_index,
                    "valid": text is not None and anchor_index is not None,
                }
            )
        fields[name] = {
            "allowed_value": got in rule["allowed"],
            "correct": got == rule["expected"],
            "evidence_ok": any(item["valid"] for item in evidence_results),
            "evidence": evidence_results,
            "observed": got,
        }

    elapsed = answer.get("elapsed_seconds")
    elapsed_valid = isinstance(elapsed, (int, float)) and not isinstance(elapsed, bool) and elapsed >= 0
    within_time = elapsed_valid and elapsed <= contract["time_limit_seconds"]
    identity_ok = answer.get("target_commit") == commit
    facts_ok = all(item["allowed_value"] and item["correct"] for item in fields.values())
    evidence_ok = all(item["evidence_ok"] for item in fields.values())
    passed = source_commit_ok and identity_ok and within_time and facts_ok and evidence_ok
    return {
        "contract_version": contract["contract_version"],
        "target_project": contract["target_project"],
        "passed": passed,
        "source_commit_ok": source_commit_ok,
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
    parser.add_argument("answer")
    parser.add_argument("--target-repo", required=True)
    parser.add_argument("--contract", default=str(Path(__file__).with_name("contract-v3.json")))
    args = parser.parse_args()
    try:
        result = score(load_json(args.contract), load_json(args.answer), Path(args.target_repo).resolve())
    except (ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
