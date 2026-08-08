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
