# C04 — Enforcement

Status: SHIPS

## User job

Rules that matter are checks. A green that would stay green if the thing were broken is
treated as a bug.

## Deliverable

`python scripts/sabotage_test.py` — 18/18 seeded defects detected.
`rules/LEDGER.md` maps ideas to checks.

## Output location

`scripts/onboard_check.py`, `scripts/sabotage_test.py`, `workflow/blueprint/rules/LEDGER.md`

## Quality bar

Law 2: every ENCODED row names a check that fails a fixture. selftest fails the ledger if
an ENCODED row has no check path.

## Remaining work

Recurrence tracking (the playbook headline is unverified). That is the measurement the
enforcement invariant exists to create.

## Taken from

LAWS 1–2; RULES-LEDGER; ARCHITECTURE enforcement invariant.
