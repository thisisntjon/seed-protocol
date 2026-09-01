#!/usr/bin/env python3
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

p = Path(__file__).resolve().parent / "artifacts"
rows = [
    json.loads(line)
    for line in (p / "pr_index.jsonl").read_text(encoding="utf-8").splitlines()
    if line.strip()
]
s = json.loads((p / "summary.json").read_text(encoding="utf-8"))
start = datetime.fromisoformat(min(r["when"][:10] for r in rows))
buckets = defaultdict(Counter)
for r in rows:
    d = datetime.fromisoformat(r["when"][:10])
    key = (start + timedelta(days=((d - start).days // 7) * 7)).date().isoformat()
    buckets[key][r["file_class"]] += 1
    buckets[key]["n"] += 1
print("n", len(rows))
print("weekly")
weekly = {}
for k in sorted(buckets):
    c = buckets[k]
    n = c["n"]
    weekly[k] = dict(c)
    print(
        f"  {k} n={n:4d} docs={c['docs_only']/n:5.1%} "
        f"code={c['has_code']/n:5.1%} other={(n-c['docs_only']-c['has_code'])/n:5.1%}"
    )
ch = sorted(r["churn"] for r in rows)

def pct(q):
    return ch[int(q * (len(ch) - 1))]

print("churn p50", pct(0.5), "p90", pct(0.9), "p99", pct(0.99), "max", ch[-1])
merged = s["github"]["pr_merged"]
print("coverage", round(len(rows) / merged, 4))
rev = json.loads((p / "review_sample.json").read_text(encoding="utf-8"))
s["review_sample"] = {
    "k": rev["k"],
    "with_any_review": rev["with_any_review"],
    "with_human_review": rev["with_human_review"],
    "review_logins": rev["review_logins"],
    "independent_human_not_author": 0,
    "note": "the sole human reviewer login in the sample is thisisntjon, the PR author",
}
s["github_merged_coverage"] = round(len(rows) / merged, 4)
s["weekly"] = weekly
s["churn"] = {"p50": pct(0.5), "p90": pct(0.9), "p99": pct(0.99), "max": ch[-1]}
s["direct_main_not_pr_token"] = s["n_first_parent_skipped_no_pr_token"]
(p / "summary.json").write_text(json.dumps(s, indent=2) + "\n", encoding="utf-8")
print("wrote summary")
