# C17 — Non-destructive transplant

Status: SHIPS

## User job

Install CORE into an existing project without overwriting its identity.

## Deliverable

`python scripts/transplant.py --target <git> --apply`

Refuses differing files. Records hashes in `workflow/SEED-TRANSPLANT.json`.
