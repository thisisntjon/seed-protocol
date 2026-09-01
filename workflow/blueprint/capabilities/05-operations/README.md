# C05 — Operations

Status: PARTIAL

## User job

Unattended work: spend is metered, long jobs checkpoint, silence is not health, QoL so
jobs are resumable.

## Deliverable

Optional: `scripts/spend_check.py`, `scripts/stress_test.py`. Checklist: qol-baseline 22
items (N/A is valid). TOOL-REBUILD tiers 3–4.

## Output location

`scripts/spend_check.py`, `scripts/stress_test.py`, `../harvest/pack/candidate/TOOL-REBUILD.md`

## Quality bar

Spend window with zero closed loops fails. Stress test: 100% detection, 0 false alarms on
its registered seeds.

## Remaining work

OS-scheduled digest and queue_worker — encode when jobs outlive sessions (I-G02, I-G06).

## Taken from

TOOLS.md tier 3; COST.md; qol-baseline; harvest H/J/G.
