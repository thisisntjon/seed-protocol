#!/usr/bin/env python3
"""Count how often PR numbers from the census appear in protocol artifacts."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

PIN_INDEX = Path(__file__).resolve().parent / "artifacts" / "pr_index.jsonl"
POKE = Path(r"C:\Users\thisi\Desktop\Pokemon")
PR_RE = re.compile(r"#(\d{1,4})\b")

# Surfaces that would implement "incident → check" if the join existed.
ROOTS = [
    POKE / "workflow",
    POKE / "playbook",
    POKE / "ptcg-agent" / "docs",
]


def iter_md(root: Path):
    if not root.exists():
        return
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".json", ".py"}:
            continue
        if ".git" in path.parts:
            continue
        yield path


def main() -> None:
    prs = set()
    for line in PIN_INDEX.read_text(encoding="utf-8").splitlines():
        if line.strip():
            prs.add(json.loads(line)["pr"])
    hits = Counter()
    files_hit = Counter()
    cited = set()
    by_bucket = Counter()
    for root in ROOTS:
        bucket = root.name
        for path in iter_md(root):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            found = {int(x) for x in PR_RE.findall(text)}
            found &= prs
            if not found:
                continue
            rel = str(path.relative_to(POKE)).replace("\\", "/")
            for n in found:
                hits[n] += 1
                cited.add(n)
            files_hit[rel] += len(found)
            by_bucket[bucket] += len(found)
    # special files
    special = {}
    for rel in (
        "playbook/RULES-LEDGER.md",
        "playbook/PLAYBOOK.md",
        "workflow/DEAD-ENDS.md",
        "workflow/GATES.md",
        "ptcg-agent/docs/EVAL_PROTOCOL.md",
    ):
        path = POKE / rel
        if not path.exists():
            special[rel] = None
            continue
        found = {int(x) for x in PR_RE.findall(path.read_text(encoding="utf-8", errors="replace"))}
        special[rel] = {
            "raw_tokens": len(found),
            "in_census": len(found & prs),
        }
    out = {
        "census_n": len(prs),
        "cited_in_protocol_tree": len(cited),
        "cite_rate": round(len(cited) / len(prs), 4) if prs else None,
        "by_root": dict(by_bucket),
        "top_files": files_hit.most_common(15),
        "special": special,
        "uncited": len(prs) - len(cited),
    }
    dest = Path(__file__).resolve().parent / "artifacts" / "pr_join.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2)[:4000])


if __name__ == "__main__":
    main()
