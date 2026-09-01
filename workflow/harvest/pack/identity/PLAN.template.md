# PLAN — living document

Format: phased-investigation-workflow (`/phased`).
Triage depth: **Light | Standard | Deep** — pick one and delete the others.
Current stage: frame
Last updated: YYYY-MM-DD

## Problem

**Problem:** (one paragraph)

**Why now:** (one paragraph)

**Original hypothesis:**

> (the sentence being tested)

## Goal

(one paragraph, observable)

## Success criteria

1. `python scripts/onboard_check.py` exits 0.
2. `python scripts/sabotage_test.py` proves the checker fails on each seeded defect class.
3. (project-specific measured outcome)

## Assumption registry

- Assumption: (load-bearing belief)
  Source: (file or incident)
  Status: holding | flipped | unverified
  | Affects: (which phases)

## Phasing

<!-- Status column machine-parsed by scripts/status.py: DONE | ACTIVE | ACTIVE(nn%) | TODO -->

| Phase | Scope | Gate | Status |
|---|---|---|---|
| P1 Identity | Fill START-HERE four lines and this problem statement | onboard_check green; sabotage_test proves red-on-defect | TODO |
| P2 First loop | One dispatch, one receipt, one handoff | receipt banks with evidence | TODO |
| P3 (name later) | (coarse until P2 closes) | (named measurement) | TODO |

### Phase 1 — Identity  [status: pending]
**Produces:** truthful START-HERE + this PLAN
**Verifies:** `python scripts/onboard_check.py`

## Research

(links to `workflow/research/` findings; conversation is not the record)
