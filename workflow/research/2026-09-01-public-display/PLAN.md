# Public-display investigation — living plan

Format: `/phased`. Triage: **Medium** — the contest-readiness score (47/100) and
Pokemon operating loop are already known; this investigation decides the *public
object*, not whether SEED is causally useful.
Current stage: parallel investigation (T-001–T-005), then synthesis (T-006)
Last updated: 2026-09-01

## Problem

thefleet is a private measurement protocol with a green CI and an honest README.
A mixed contest panel would score it ~47/100. Pokemon *operates* the loop
(poll → claim-by-push → verdict PR → bus receipt → hash-pinned gate) but is a
private mill (~683 harness scripts, hub 4787 ahead of origin/main). Importing
that mill would drop the score. We need one public-display version that a
stranger can name, run, and trust — as close to 100 as the evidence allows.

## Goal

A single synthesis (`SPEC.md`) that names, file-by-file, what the public tree
adds, changes, and omits. Implementation is a later board. This investigation
does not flip repo visibility (GATES publication).

## Success criteria

1. Five independent briefs exist (FRONT-DOOR, HYGIENE, DEMO, EVIDENCE, SCOPE).
2. SPEC.md estimates post-change score and the remaining unbuyable gap.
3. C-004 stays HYPOTHESIS unless a brief finds a already-run ablation (it will not).
4. `python scripts/onboard_check.py` still passes after any files this investigation adds.
5. No ticket edits README.md, LICENSE, or verify.yml — those wait for the build board.

## Assumption registry

- Assumption: 100 on a mixed panel is only reachable if the entry is scored as
  the instrument, not as a proven treatment effect.
  Status: holding | Affects: JUDGES.md copy; badge text
- Assumption: poketcg remains private; `artifacts/` is the public dataset.
  Status: holding (gh: isPrivate true, 2026-08-31) | Affects: EVIDENCE, Reproduce
- Assumption: MVS is solo + two agents; fleet mailbox is out of the public object.
  Source: playbook/BOOTSTRAP.md; DECISIONS 2026-08-08
  Status: holding | Affects: SCOPE, DEMO

## Phasing

| Phase | Scope | Status |
|---|---|---|
| I0 Board | board/ + these tickets | ACTIVE |
| I1 Parallel briefs | T-001–T-005 | TODO |
| I2 Synthesis | T-006 SPEC.md | TODO (depends I1) |
| I3 Build | later board — implement SPEC | not this investigation |
