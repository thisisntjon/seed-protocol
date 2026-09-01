# Blueprint build — living document

Format: `/phased`. Triage: **Light** (hardening list is well-understood; failure mode is
sprawl, prevented by NEVER mill / no spend / no PORTABLE_FILES growth).
Current stage: hardening — H1 landing in CI; H2 is the next build
Last updated: 2026-08-31

> Does **not** replace paused SEED `workflow/PLAN.md`. Does **not** replace harvest
> `workflow/harvest/PLAN.md`. This file is the factory's own build plan.

## Problem

**Problem:** ~$120k of recovered portable yield (executable protocol + named mistakes +
expected avoided waste) sits in a catalog that CI does not bind, that a second machine
cannot copy without path edits, and that measurement rules will not fire because they are
prose. Unused insurance expires.

**Why now:** Extract and ideas ledger are done. Further file-by-file harvest has diminishing
returns. Hardening is how the $120k stays real.

**Original hypothesis:** (Jon, 2026-08-23)

> How do we harden that value? Please think of 10 things we should do in the bonkers
> project to increase the value. These should be real high value opportunities that are
> low risk.

## Goal

Ten small, reversible moves in this repo such that: the factory cannot rot in silence, a
clean dest still onboards, measurement tripwires have sabotage fixtures, and a vendor
switch has an escrow+paste path — without importing the mill or spending money.

Detail and done-when: `HARDENING.md`.

## Success criteria

1. `HARDENING.md` lists exactly ten items, each with a green command.
2. H1–H2: `selftest.py` fails if a capability README or bootstrap dest onboard breaks;
   CI runs selftest + assemble --check + orient.
3. H7: three seeded defects (skipped-pass, switch/claim drift, receipt without evidence
   path) turn a guard red.
4. `python scripts/onboard_check.py` and `python scripts/sabotage_test.py` still pass
   after each item.
5. `scripts/transplant.py` PORTABLE_FILES unchanged.

## Assumption registry

- Assumption: Light triage is enough; the ten items are known, not researched.
  Source: extract + catalog + Miracle pattern already banked
  Status: holding
  | Affects: skip Deep investigation

- Assumption: CI + dogfood + three tripwires lock more value than another extract pass.
  Source: 2026-08-23 value memo (composition and a live loop dominate)
  Status: unverified until H1–H2 exist
  | Affects: sequencing H1 first

- Assumption: switch.py escrow is low risk (local git refs, no push, no spend).
  Source: ARCHITECTURE layer 3 gap
  Status: holding
  | Affects: H8

- Assumption: P3 ablation is the wrong tool to harden $120k now.
  Source: C-004 pending; GATES spend
  Status: holding
  | Affects: exclusion list

## Phasing

| Phase | Scope | Gate | Status |
|---|---|---|---|
| B0 Extract | File-by-file log | EXTRACT-LOG complete | DONE |
| B1 Catalog + v1 bins | capabilities + orient/bootstrap/selftest | selftest green; onboard green | DONE |
| H1 CI bind | verify.yml + selftest/assemble/orient | deleting a capability README fails CI | DONE 2026-08-31 |
| H2 Bootstrap round-trip | selftest temp dest onboard+orient | fixture red on broken assemble | TODO |
| H3 Event jsonl | orient/selftest/bootstrap append | cap + grep | TODO |
| H4 Recipes | greenfield / incident / promotion | dry-run prints commands | TODO |
| H5 Path-free skills | phased + handoff copies | no C:\Users\thisi in copies | TODO |
| H6 Budget/approval objects | templates; spend_check skip if absent | missing BUDGET ≠ onboard red | TODO |
| H7 Measure tripwires | three guards + sabotage | 3/3 red fixtures | TODO |
| H8 switch.py | escrow + paste boot | restore dirty tree | TODO |
| H9 conventions.yml | single source; START-HERE string check | drift fails selftest | TODO |
| H10 Handoff + C-006 | short handoff; claim bound after H2 | onboard green | TODO |
| B2 Switch adapters | full render.py | after H8/H9 | TODO (deferred) |
| B3 Fleet module | templates/fleet | second-agent incident | TODO (deferred) |

Execute **H1 then H2 then H7** as the lock. H10 handoff can run beside H1. Do not start
H8 until H1 is green (continuity on a rotting CI is wasted).

## Research

- `HARDENING.md` — the ten items
- `CAPABILITY-CATALOG.md` — PARTIAL rows this sequence closes
- Miracle: deliverables/approval-gates, budget-scorecards, workflow-ledger (pattern only)
