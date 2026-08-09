#!/usr/bin/env python3
"""Verify a v2 contract's source blobs against the exact target git commit."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_repo")
    parser.add_argument("--contract", default=str(Path(__file__).with_name("contract-v2.json")))
    args = parser.parse_args()
    contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
    target = Path(args.target_repo).resolve()
    results = {}
    for path, expected_oid in contract["sources"].items():
        proc = subprocess.run(
            ["git", "-C", str(target), "rev-parse", f"{contract['target_commit']}:{path}"],
            capture_output=True,
            text=True,
        )
        observed = proc.stdout.strip() if proc.returncode == 0 else None
        results[path] = {
            "expected_blob_oid": expected_oid,
            "observed_blob_oid": observed,
            "correct": observed == expected_oid,
        }
    passed = all(item["correct"] for item in results.values())
    print(json.dumps({"passed": passed, "target_commit": contract["target_commit"], "sources": results}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
