#!/usr/bin/env python3
"""Draw a stratified 80-PR sample and apply a published intent codebook (pass 1).

Pass 1 is rule-based on subject + paths. Pass 2 (hand) is applied in
artifacts/sample80_pass2.jsonl after inspection. Disagreement is the dual-pass.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

PIN = "9522a8a37078d00f46b99a586b825b789b01387d"
REPO: Path | None = None
HERE = Path(__file__).resolve().parent
N_PER = 20


def git(*args: str) -> str:
    if REPO is None:
        raise RuntimeError("clone path not set; pass it as the first argument")
    r = subprocess.run(
        ["git", "-C", str(REPO), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    return r.stdout


def paths_for(sha: str) -> list[str]:
    out = git("diff-tree", "--no-commit-id", "--name-only", "-r", sha)
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def intent(subject: str, paths: list[str]) -> str:
    s = subject.lower()
    joined = " ".join(paths).replace("\\", "/").lower()
    ev_kw = (
        "receipt", "experiment", "eval", "gate", "bank", "evidence", "null",
        "killed", "pre-reg", "prereg", "sabotage", "census",
    )
    gov_kw = (
        "kanban", "inbox", "mailbox", "roster", "orchestrat", "status.json",
        "board", "protocol", "agents.md", "gates.md",
    )
    cer_kw = (
        "cycle log", "cycle-log", "typo", "whitespace", "changelog",
        "catch up", "docs catch", "refresh docs", "handoff memo",
    )
    n_py = sum(1 for p in paths if p.endswith(".py"))
    n_md = sum(1 for p in paths if p.endswith(".md") or p.endswith(".txt"))
    n_test = sum(1 for p in paths if "test_" in Path(p).name or "/test" in p.replace("\\", "/"))
    if any(k in s for k in cer_kw) and n_py == 0:
        return "CEREMONY"
    if n_test and n_py:
        return "EVIDENCE"
    if any(k in s for k in ev_kw) or "experiments/" in joined or "receipts/" in joined:
        if n_py:
            return "MIXED"
        return "EVIDENCE"
    if any(k in s for k in gov_kw) or "workflow/" in joined and n_py == 0:
        return "GOVERNANCE"
    if n_py and n_md and n_py >= 1 and n_md >= 3:
        return "MIXED"
    if n_py:
        return "CONSTRUCTION"
    if n_md and not n_py:
        if any(k in s for k in ("fix", "implement", "add ", "harness", "agent")):
            return "GOVERNANCE"
        return "GOVERNANCE"
    return "OTHER"


def draw() -> list[dict]:
    rows = [
        json.loads(line)
        for line in (HERE / "artifacts" / "pr_index.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    by = {"docs_only": [], "has_code": [], "other": []}
    for row in rows:
        fc = row.get("file_class")
        if fc in by:
            h = hashlib.sha256((PIN + str(row["pr"])).encode()).hexdigest()
            by[fc].append((h, row))
    sample = []
    for fc, bucket in by.items():
        bucket.sort()
        take = bucket[:N_PER]
        # extra 20 from remaining has_code+docs mixed by hash for small-vs-large
        for h, row in take:
            sample.append(row)
    # 20 additional small PRs not already sampled
    have = {r["pr"] for r in sample}
    small = []
    for row in rows:
        if row["pr"] in have:
            continue
        if row.get("small"):
            h = hashlib.sha256((PIN + "small" + str(row["pr"])).encode()).hexdigest()
            small.append((h, row))
    small.sort()
    for h, row in small[:N_PER]:
        sample.append(row)
    return sample


def main() -> None:
    global REPO
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        sys.exit("usage: label_sample.py <poketcg-clone>")
    REPO = Path(sys.argv[1])
    sample = draw()
    labeled = []
    for row in sample:
        paths = paths_for(row["sha"])
        lab = intent(row["subject"], paths)
        labeled.append(
            {
                "pr": row["pr"],
                "sha": row["sha"],
                "when": row["when"],
                "subject": row["subject"],
                "file_class": row["file_class"],
                "churn": row["churn"],
                "n_files": len(paths),
                "paths_head": paths[:12],
                "pass1_intent": lab,
            }
        )
    out = HERE / "artifacts" / "sample80_pass1.jsonl"
    out.write_text("\n".join(json.dumps(x) for x in labeled) + "\n", encoding="utf-8")
    print("wrote", out, "n", len(labeled))
    print(json.dumps(Counter(x["pass1_intent"] for x in labeled), indent=2))
    print(json.dumps(Counter(x["file_class"] for x in labeled), indent=2))


if __name__ == "__main__":
    main()
