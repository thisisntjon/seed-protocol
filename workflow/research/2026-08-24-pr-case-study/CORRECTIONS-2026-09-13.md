# Census precision correction — 2026-09-13

This correction updates the current [paper](PAPER.md), the repository README's reviewer description and the archive notice on [REPORT.md](REPORT.md). The raw public datasets, method scripts, original source pin and research question are unchanged. Root reviews and publishes the prepared patch; this record is not a new census run or independent reproduction of the private-source instrument.

**Baseline repository:** `822fe1a1e1986edaed47db65296d95e69fbcbd5c`. **Census source pin recorded in the public artifacts:** `9522a8a37078d00f46b99a586b825b789b01387d`.

| Question | Existing public evidence and correction | Why the former interpretation failed |
|---|---|---|
| Which week had the smallest code share? | `summary.json` → `weekly`: July 8 has 194/652 = 29.7546%, reported as 29.75%; July 15 has 139/488 = 28.4836%, reported as 28.48%. July 8 has the most landings; July 15 has the lowest code share among the seven listed weeks. | A maximum in volume was mistaken for a minimum in a different metric. |
| What changed by August 12? | Code share is 61/79 = 77.2152%, while the code-containing commit count fell from July 8's 194 to 61. | A rising proportion does not establish more construction, greater value or improved gameplay. |
| Did earlier estimates reproduce exactly? | Current docs-only is 855/1,979 = 43.2036%; small churn is 786/1,979 = 39.7170%. The rounded current values, 43.2% and 39.7%, update earlier 44.7% and 39.6% estimates. | Numerical proximity across snapshots was described as identical reproduction. |
| How many sampled PRs had bot reviews? | `review_sample.json` rows: 40 PRs; 17 have any review; all 17 have `chatgpt-codex-connector[bot]` in `review_logins`. PR #2377 also has a review from its author, `thisisntjon`. Independent human reviewers other than the PR author: 0/40. | Bot and human review categories overlap; subtracting the human-reviewed PR from all reviewed PRs dropped one bot-reviewed PR. |
| Was code oversampled? | `sample80_pass2.jsonl`: 33 docs-only, 24 code-containing and 23 other records. The sample code share is 24/80 = 30.0%, below the census 761/1,979 = 38.4538%. | The paper inferred the realized composition from the sampling description instead of counting the saved sample. |
| What does 2/80 PRODUCT estimate? | `sample80_summary.json` and the 80 labelled records report 2 PRODUCT, 29 EVIDENCE, 26 GOVERNANCE, 15 INSTRUMENT, 4 CEREMONY and 4 OTHER. The unweighted 2.5% describes this stratified sample only. | Neither a population weighting analysis nor a statistical bound was established. Direct policy edits also do not exhaust useful project contributions. |
| Can file composition prove a stagnant player or bound useful output below a majority? | The codebook classifies changed file types; the intent labels describe one inspector's sample. The corrected paper requires separate outcome evidence for player improvement and work value. | File suffixes and edit locations are not outcome measurements or an upper bound on research value. |
| Does the stated first-parent total reconcile? | `summary.json` separately reports 1,979 PR-linked commits and 2,106 skipped no-token records. Their arithmetic sum is 4,085, not the former 4,093. The paper retains the two classified counts but asserts no verified whole-history total. | The available public summary does not establish a reconciliation of the earlier total; inventing missing records would exceed the evidence. |

The composition table now also displays the instrument's one `empty` record, so its file-class rows account for all 1,979 records. The small-churn row is an overlapping property, not an additional disjoint class.

## Verification method and limits

Read the saved JSON/JSONL with Python's standard library, count review logins and sample classes, and divide weekly counts by their recorded denominators. Check the rendered prose against those results. No source-repository census, GitHub review collection, relabelling, model call, gameplay experiment or generator execution was performed. In particular, `postprocess.py` writes `summary.json`, so it was inspected but not run.

Recorded SHA-256 values of the inspected public artifacts, before editing:

| File under `artifacts/` | SHA-256 |
|---|---|
| `summary.json` | `6f70cabdf85729b81e8274d8f03b52766d664e2a3e44e122567a32aeecafe75b` |
| `review_sample.json` | `3e67ae8dbbfccbc9012a773ee9c2d6b92bccf2cbe9747eccf8b3e99cbaf04038` |
| `sample80_summary.json` | `030fd18c2fb873e9774f5e578938a12005700c860952dcfcdad0c9e99fdf68ae` |
| `pr_index.jsonl` | `14a7f16c8d48088b19a48d674903c6fb4be9bfe4f276e57c817d6bd6c7070e06` |
| `sample80_pass2.jsonl` | `803456e2ef16770a648e7ab8268a1540f33b6ef86539a5ca4fd575e88e6725c0` |

The earlier memo's body is preserved with a top correction notice. Current statements belong in PAPER.md; the global retraction ledger links this scoped correction and rejects three exact superseded paper statements. Broader protocol claims, literature comparisons, private-source reproducibility and causal benefit of SEED were outside this correction.

Reopen only if another check finds a mismatch in the saved evidence, the original instrument's author establishes the first-parent reconciliation, or a separately reviewed weighted/independent analysis changes the admissible interpretation.
