# RETRACTIONS — numbers and claims that are in the record as FALSE

Copy this file into a target repo as the token ledger. Fill rows from **this** project's
incidents. Do not import another project's retracted values.

**Check this file before citing any figure.**

Rules:
- A retraction names the false value, what to use instead, and the MECHANISM that produced the
  error — mechanisms recur; corrections don't transfer without them.
- If a generator emits it, fix the generator in the same change.
- `scripts/onboard_check.py` fails the repo if a retracted token below is cited in any
  markdown outside this file.

<!-- RETRACTIONS-TABLE machine-parsed by scripts/onboard_check.py
     token = the exact string that must not appear elsewhere -->

| token | use instead | why it was wrong (mechanism) | retracted |
|---|---|---|---|

## How to retract

1. Add the row with a replacement and a reason.
2. If a generator emits it, patch the generator in the same change.
3. Correct the source by editing, not a banner underneath.
