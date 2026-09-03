# RETRACTIONS — numbers that are in the record but FALSE

Check this file before citing ANY number from an older document. This repo corrects by editing
(Law 6), but anything already quoted elsewhere lands here when it dies. Rows are never deleted.

Rules:
- A retraction names the false value, what to use instead, and the MECHANISM that produced the
  error — mechanisms recur; corrections don't transfer without them.
- If a dashboard/script REGENERATES a retracted value, patch the generator, not the output, and
  note the generator here until patched.
- `scripts/onboard_check.py` fails the repo if a retracted token below is cited in any tracked
  markdown outside this file.

<!-- RETRACTIONS-TABLE machine-parsed by scripts/onboard_check.py
     token = the exact string that must not appear elsewhere -->

| token | use instead | why it was wrong (mechanism) | retracted |
|---|---|---|---|
| EXAMPLE-999.9 | (delete this example row on first real retraction) | Example mechanism: frozen pre-maturity artifact quoted as converged | 2026-08-08 |
| ~14 files | small, incident-bounded core; actual file count is descriptive, not a target | Approximate component count was published as a file-count constraint before the first git identity existed | 2026-08-08 |
| sabotage_test: 5/5 | use the newest receipt bound to an exact commit | The stale-gate sabotage depended on an existing OPEN gate and stopped testing its claimed defect after that gate was answered | 2026-08-08 |
| 49,686 | no dollar figure; Law 9 is stated without one | `~$49,686` was published (commit 87171d5, 2026-08-08) in LAWS.md Law 9, DECISIONS.md, and the `scripts/spend_check.py` docstring as the API-list-equivalent spend that earned Law 9. Two independent audits of the source project could not find the figure there, and the cited source `playbook/COST.md` has empty dollar cells; the number was quoted as metered fact without a generator or a receipt behind it. Marked unverified in DECISIONS.md on 2026-08-18; entered here as retracted because a figure with no locatable source is not citable. Do not invent a substitute dollar | 2026-09-02 |
| 49.7k | no dollar figure; Law 9 is stated without one | `$49.7k` is the rounded form of the same figure (commit 87171d5 subject line, `workflow/receipts/2026-08-08-law9-spend-lesson.md`). Same mechanism: rounding a number that was never verified does not make it verified | 2026-09-02 |
