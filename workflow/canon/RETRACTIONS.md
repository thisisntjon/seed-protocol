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
