# START HERE — machine-checked onboarding

**Rule of this file: it contains no sentence that a later sentence corrects. If reality changes,
this file is edited, not appended. `scripts/onboard_check.py` verifies its claims in CI.**

## THE WHOLE JOB, IN FOUR LINES

```
1. This repo is PROJECT-NAME. Fill this line with the actual job before any other work.
2. Read LAWS.md, AGENTS.md, GATES.md, and workflow/PLAN.md.
3. Run: python scripts/onboard_check.py   — it must pass before you act on anything written here.
4. Humans decide only what GATES.md lists. Everything else: proceed, leave receipts.
```

## Current effort (read this before the rest)

Replace this paragraph with the one current effort. One effort, named, with a path to its plan.
Do not stack superseded banners here.

## What this is

A small protocol (SEED) transplanted as the epistemic control plane, not the product runtime.
Its three commitments:

- **Preserves inspectable state** — decisions and work state live in git artifacts with validated
  schemas (`workflow/templates/`), not only in chat or human memory.
- **Researches appropriately** — work begins with a phased plan (`workflow/PLAN.md`): problem,
  assumption registry with kill criteria, synthesis gate, then roadmap.
- **Supports agent-led execution** — agents propose, build, verify, and bank while humans
  remain the escalation surface for irreversibles (`GATES.md`).

## File map (every path below is verified by the checker)

| Path | What it is |
|---|---|
| `LAWS.md` | The proven laws, each with provenance and enforcement |
| `CLAIMS.md` | Falsifiable public claims, status, falsifier, and bound evidence |
| `AGENTS.md` | Universal worker contract |
| `GATES.md` | Human-key boundary + machine-parsed gate registry with SLA |
| `workflow/PLAN.md` | Living phased plan — the current effort |
| `workflow/canon/RETRACTIONS.md` | Ledger of numbers that are in the record but FALSE |
| `workflow/canon/DECISIONS.md` | Settled decisions — do not re-litigate |
| `workflow/templates/DISPATCH.md` | Schema for handing work to an agent |
| `workflow/templates/RECEIPT.md` | Schema for reporting work done |
| `workflow/templates/HANDOFF.md` | Cold-open session handoff memo format |
| `workflow/templates/EXPERIMENT.md` | Pre-registration + kill-bar template |
| `workflow/dispatches/` | Validated work claims |
| `workflow/experiments/` | Validated experiment registrations |
| `workflow/receipts/` | Banked receipts land here |
| `workflow/handoffs/` | Dated handoff memos land here |
| `scripts/onboard_check.py` | Verifies this documentation against reality |
| `scripts/sabotage_test.py` | Proves the checker fails on seeded defects |
| `scripts/status.py` | Computes phase status from artifacts |
| `scripts/checkpoint.py` | Refuses a git checkpoint while required checks are red |
| `scripts/transplant.py` | Non-destructively installs CORE into another clean git repo |

## Onboarding a fresh harness (any vendor)

1. Run `python scripts/onboard_check.py` and `python scripts/sabotage_test.py`. Red means a
   claimed invariant or its refutation test is broken — fix that first.
2. Read `LAWS.md`, `AGENTS.md`, `GATES.md`, `workflow/PLAN.md`, and the newest file in
   `workflow/handoffs/` (if any). That is the complete state.
3. Check `workflow/canon/RETRACTIONS.md` before citing ANY number found in older documents.
4. Claim work per `AGENTS.md`, do it, bank a receipt per the template, update the handoff.

Last verified against reality: fill on first passing check.
