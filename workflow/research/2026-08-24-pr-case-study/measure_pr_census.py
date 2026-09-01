#!/usr/bin/env python3
"""Census squash-merged PRs on a pinned first-parent history.

Stdlib + git + optional gh. Writes JSON artifacts next to this script.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


PIN_SHA = "9522a8a37078d00f46b99a586b825b789b01387d"
PR_END_RE = re.compile(r"\(#(\d+)\)\s*$")
PR_MERGE_RE = re.compile(r"Merge pull request #(\d+)", re.I)


def extract_pr(subject: str) -> int | None:
    match = PR_END_RE.search(subject)
    if match:
        return int(match.group(1))
    match = PR_MERGE_RE.search(subject)
    if match:
        return int(match.group(1))
    return None
DOC_EXT = {".md", ".txt"}
CODE_EXT = {".py", ".go", ".js", ".ts", ".rs", ".java", ".c", ".cpp", ".h"}
CLASS_TOKENS = ("[bank]", "[ops]", "[instrument]", "[research]")


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or "git failed: " + " ".join(args))
    return result.stdout


def gh_json(*args: str):
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or "gh failed")
    return json.loads(result.stdout) if result.stdout.strip() else None


def classify_files(paths: list[str]) -> str:
    if not paths:
        return "empty"
    exts = [Path(p).suffix.lower() for p in paths]
    if all(ext in DOC_EXT for ext in exts):
        return "docs_only"
    if any(ext in CODE_EXT for ext in exts):
        return "has_code"
    return "other"


def title_class(subject: str) -> str:
    lower = subject.lower()
    for token in CLASS_TOKENS:
        if token in lower:
            return token
    return "none"


def census(repo: Path, out_dir: Path) -> dict:
    head = git(repo, "rev-parse", PIN_SHA).strip()
    if head != PIN_SHA:
        raise RuntimeError(f"pin missing: wanted {PIN_SHA} got {head}")
    log = git(
        repo,
        "log",
        PIN_SHA,
        "--first-parent",
        "--pretty=format:COMMIT\t%H\t%aI\t%an\t%s",
        "--numstat",
    )

    def close(cur, added, deleted, paths, bucket):
        if cur is None:
            return
        cur["additions"] = added
        cur["deletions"] = deleted
        cur["paths"] = paths
        cur["churn"] = added + deleted
        cur["file_class"] = classify_files(paths)
        cur["title_class"] = title_class(cur["subject"])
        cur["small"] = cur["churn"] < 100
        bucket.append(cur)

    commits = []
    current = None
    added = deleted = 0
    paths: list[str] = []
    skipped_no_pr = 0
    for line in log.splitlines():
        if line.startswith("COMMIT\t"):
            close(current, added, deleted, paths, commits)
            _tag, sha, when, author, subject = line.split("\t", 4)
            pr_n = extract_pr(subject)
            if pr_n is None:
                skipped_no_pr += 1
                current = None
                added = deleted = 0
                paths = []
                continue
            current = {
                "sha": sha,
                "when": when,
                "author": author,
                "subject": subject,
                "pr": pr_n,
            }
            added = deleted = 0
            paths = []
            continue
        if current is None or not line.strip():
            continue
        ns = re.match(r"^(\d+|-)\t(\d+|-)\t(.+)$", line)
        if ns:
            a, d, path = ns.group(1), ns.group(2), ns.group(3)
            if a != "-":
                added += int(a)
            if d != "-":
                deleted += int(d)
            paths.append(path)
    close(current, added, deleted, paths, commits)

    by_pr = {}
    for row in commits:
        if row.get("pr") is None:
            continue
        by_pr[row["pr"]] = row

    n = len(by_pr)
    file_class = Counter(r["file_class"] for r in by_pr.values())
    title_class_c = Counter(r["title_class"] for r in by_pr.values())
    authors = Counter(r["author"] for r in by_pr.values())
    small_n = sum(1 for r in by_pr.values() if r["small"])
    docs_n = file_class.get("docs_only", 0)
    days = Counter(r["when"][:10] for r in by_pr.values())
    peak_day, peak_n = max(days.items(), key=lambda kv: kv[1]) if days else ("", 0)

    authors_main = git(repo, "log", PIN_SHA, "--pretty=%an").splitlines()
    authors_all = git(repo, "shortlog", "-sn", "--all")
    all_names = []
    for line in authors_all.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t" if "\t" in line else None, 1)
        if len(parts) == 2:
            all_names.append(parts[1].strip())
        else:
            all_names.append(re.sub(r"^\s*\d+\s+", "", line).strip())

    summary = {
        "pin_sha": PIN_SHA,
        "n_first_parent_pr_commits": n,
        "n_first_parent_skipped_no_pr_token": skipped_no_pr,
        "docs_only": docs_n,
        "docs_only_rate": round(docs_n / n, 4) if n else None,
        "small_lt_100": small_n,
        "small_rate": round(small_n / n, 4) if n else None,
        "has_code": file_class.get("has_code", 0),
        "other_files": file_class.get("other", 0),
        "empty": file_class.get("empty", 0),
        "file_class": dict(file_class),
        "title_class": dict(title_class_c),
        "squash_authors": dict(authors),
        "unique_authors_origin_main_log": len(set(a for a in authors_main if a)),
        "unique_authors_shortlog_all": len([a for a in all_names if a]),
        "shortlog_all_names": all_names,
        "n_days_with_pr": len(days),
        "peak_day": peak_day,
        "peak_day_n": peak_n,
        "mean_pr_per_active_day": round(n / len(days), 2) if days else None,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    slim = [
        {
            "pr": r["pr"],
            "sha": r["sha"],
            "when": r["when"],
            "author": r["author"],
            "subject": r["subject"],
            "churn": r["churn"],
            "n_files": len(r["paths"]),
            "file_class": r["file_class"],
            "title_class": r["title_class"],
            "small": r["small"],
        }
        for r in sorted(by_pr.values(), key=lambda x: x["pr"])
    ]
    (out_dir / "pr_index.jsonl").write_text(
        "\n".join(json.dumps(row) for row in slim) + "\n", encoding="utf-8"
    )
    return summary, slim


def github_totals() -> dict:
    def count(q: str) -> int:
        data = gh_json("api", "-X", "GET", "search/issues", "-f", f"q={q}", "--jq", "{total:.total_count}")
        if isinstance(data, dict):
            return int(data.get("total", data.get("total_count", 0)))
        return int(data)

    # gh --jq with a map can fail; use python
    def count2(q: str) -> int:
        raw = subprocess.run(
            ["gh", "api", "-X", "GET", "search/issues", "-f", f"q={q}"],
            capture_output=True,
            text=True,
        )
        if raw.returncode != 0:
            raise RuntimeError(raw.stderr)
        return json.loads(raw.stdout)["total_count"]

    return {
        "pr_all": count2("repo:thisisntjon/poketcg is:pr"),
        "pr_merged": count2("repo:thisisntjon/poketcg is:pr is:merged"),
        "pr_closed_unmerged": count2("repo:thisisntjon/poketcg is:pr is:closed is:unmerged"),
        "pr_open": count2("repo:thisisntjon/poketcg is:pr is:open"),
    }


def review_sample(slim: list[dict], k: int = 40) -> dict:
    rng_key = PIN_SHA.encode()
    scored = []
    for row in slim:
        h = hashlib.sha256(rng_key + str(row["pr"]).encode()).hexdigest()
        scored.append((h, row))
    scored.sort()
    sample = [row for _, row in scored[:k]]
    rows = []
    logins = Counter()
    with_reviews = 0
    human_reviews = 0
    for row in sample:
        try:
            reviews = gh_json(
                "api",
                f"repos/thisisntjon/poketcg/pulls/{row['pr']}/reviews",
            )
        except RuntimeError as exc:
            rows.append({"pr": row["pr"], "error": str(exc)[:200]})
            continue
        reviews = reviews or []
        logins_here = [r.get("user", {}).get("login") for r in reviews if r.get("user")]
        for login in logins_here:
            logins[login] += 1
        human = [lg for lg in logins_here if lg and "bot" not in lg.lower() and "codex" not in lg.lower() and "copilot" not in lg.lower()]
        if reviews:
            with_reviews += 1
        if human:
            human_reviews += 1
        pr_meta = gh_json("api", f"repos/thisisntjon/poketcg/pulls/{row['pr']}")
        user = (pr_meta or {}).get("user", {}).get("login")
        rows.append(
            {
                "pr": row["pr"],
                "file_class": row["file_class"],
                "title_class": row["title_class"],
                "churn": row["churn"],
                "gh_user": user,
                "n_reviews": len(reviews),
                "review_logins": logins_here,
                "human_reviewer": bool(human),
            }
        )
    return {
        "k": k,
        "with_any_review": with_reviews,
        "with_human_review": human_reviews,
        "review_logins": dict(logins),
        "rows": rows,
    }


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = set(a for a in sys.argv[1:] if a.startswith("--"))
    if not args:
        print(
            "usage: measure_pr_census.py <poketcg-clone> [--no-reviews]",
            file=sys.stderr,
        )
        return 2
    repo = Path(args[0])
    out_dir = Path(__file__).resolve().parent / "artifacts"
    summary, slim = census(repo, out_dir)
    print(json.dumps({k: summary[k] for k in summary if k != "shortlog_all_names"}, indent=2))
    try:
        totals = github_totals()
        (out_dir / "github_totals.json").write_text(json.dumps(totals, indent=2) + "\n", encoding="utf-8")
        print("github_totals", totals)
        summary["github"] = totals
    except RuntimeError as exc:
        print("github_totals FAILED", exc)
        summary["github_error"] = str(exc)
    if "--no-reviews" in flags:
        print("review_sample SKIPPED")
        sample = None
    else:
        sample = None
        try:
            sample = review_sample(slim, 40)
        except RuntimeError as exc:
            print("review_sample FAILED", exc)
            summary["review_error"] = str(exc)
    if sample is not None:
        (out_dir / "review_sample.json").write_text(json.dumps(sample, indent=2) + "\n", encoding="utf-8")
        print(
            "review_sample",
            {k: sample[k] for k in ("k", "with_any_review", "with_human_review", "review_logins")},
        )
        summary["review_sample"] = {
            "k": sample["k"],
            "with_any_review": sample["with_any_review"],
            "with_human_review": sample["with_human_review"],
            "review_logins": sample["review_logins"],
        }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
