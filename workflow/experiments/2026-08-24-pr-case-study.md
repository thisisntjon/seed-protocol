# EXPERIMENT — PR corpus case study (pre-registration)

```
HYPOTHESIS:      Merged PR volume in thisisntjon/poketcg is a poor proxy for verified
                 product progress: a large share of merges are documentation-only or
                 under 100 lines, GitHub identity collapses to one login, and GitHub
                 reviews do not implement author-XOR-verifier.
OBJECT:          git object origin/main of thisisntjon/poketcg at SHA
                 9522a8a37078d00f46b99a586b825b789b01387d (2026-08-24T11:29:23-07:00)
                 plus GitHub PR search totals at measurement time.
DEPLOYED_FORM:   Operator-supplied clone of thisisntjon/poketcg after git fetch origin;
                 GitHub REST via `gh` authenticated as the repo owner.
MEASUREMENT:     (1) GitHub search totals: is:pr / is:merged / is:closed is:unmerged /
                 is:open. (2) First-parent commits on origin/main whose subject ends in
                 (#N): per-commit name-only list + numstat; docs-only := every path
                 ends in .md or .txt; small := additions+deletions < 100.
                 (3) Unique git authors on origin/main vs --all.
                 (4) GitHub login uniqueness on a 100-PR page of merged PRs.
                 (5) Review presence on a seeded sample of 40 merged PRs
                 (PR number hash of pin-sha, take first 40 with files).
                 (6) Title class tokens [bank] [ops] [instrument] [research].
                 Auto ceremony/construction labels are descriptive, not a PASS claim.
PASS_BAR:        File census completes for >=80% of (#N) commits; docs-only and
                 small-PR rates are reported with N; GitHub identity and review
                 samples reported. This experiment PASSes if the instrument runs;
                 it does not "pass" a product claim.
KILL_BAR:        <80% of squash commits yield a file list, or GitHub totals cannot
                 be fetched — INVALID-INSTRUMENT. Do not fall back to lore numbers.
COST:            local git + GitHub API; no model training; <1 hour wall.
OUTCOME:         PASS (instrument). Census completed on pin SHA; coverage 1979/2338 =
                 84.6% of GitHub-merged PRs (>=80% bar). docs_only 43.2% (N=1979);
                 small 39.7%. Hypothesis that volume is a poor proxy is SUPPORTED by
                 this author-run measurement, not independently reproduced.
                 Artifact: workflow/research/2026-08-24-pr-case-study/artifacts/summary.json
INDEPENDENT_REPRO: not yet. Required before citing as a non-author scientific PASS:
                 rerun measure_pr_census.py against SHA 9522a8a37078d00f46b99a586b825b789b01387d.
```

Pre-registered 2026-08-24 before census execution. Prior 44.7% / 39.6% figures are
**comparison targets**, not this run's answers.
