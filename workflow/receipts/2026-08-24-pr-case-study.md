# RECEIPT — PR corpus case study

```
STATE:       DONE
OBJECT:      workflow/research/2026-08-24-pr-case-study/PAPER.md
EXACT_REF:   poketcg-origin/main@9522a8a37078d00f46b99a586b825b789b01387d
EVIDENCE:    artifacts/summary.json docs_only_rate 0.432 small_rate 0.3972
             n=1979 PR-linked first-parent; GitHub merged 2338 coverage 0.8464;
             review_sample 0/40 independent human; python measure_pr_census.py
PROGRESS:    MEASUREMENT
EFFECT:      Camera-ready PAPER.md. Census reproduced 44.7%/39.6% as 43.2%/39.7%.
             n=80 pass2: PRODUCT 2, INSTRUMENT 15, EVIDENCE 29, GOVERNANCE 26.
             RULES-LEDGER cites 3 census PRs; KANBAN cites 301. Not independently reproduced.
BLOCKED_ON:  independent rerun of measure_pr_census.py for science-grade PASS
NEXT_OWNER:  verifier (non-author)
NEXT_EVENT:  optional dual-coded 100-PR sample; do not cite 2338 as strength
SESSION_ID:  pr-case-study-2026-08-24
```
