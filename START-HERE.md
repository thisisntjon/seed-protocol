# START HERE — machine-checked onboarding

**Rule of this file: it contains no sentence that a later sentence corrects. If reality changes,
this file is edited, not appended. `scripts/onboard_check.py` verifies its claims in CI.**

## THE WHOLE JOB, IN FOUR LINES

```
1. This repo is Bonkers; SEED is its drop-in operating protocol for AI-driven projects.
2. Read LAWS.md (the proven rules), then AGENTS.md (your contract), then workflow/PLAN.md (the work).
3. Run: python scripts/onboard_check.py   — it must pass before you act on anything written here.
4. Humans decide only what GATES.md lists. Everything else: proceed, leave receipts.
```

## What this is

A small protocol distilled from a year-long experiment (41 projects + a 30-day multi-agent
campaign, audited 2026-08-08). It is an epistemic control plane, not an agent runtime. Its three
commitments:

- **Preserves inspectable state** — decisions and work state live in git artifacts with validated
  schemas (`workflow/templates/`), not only in chat or human memory.
- **Researches appropriately** — work begins with a phased plan (`workflow/PLAN.md`): problem,
  assumption registry with kill criteria, synthesis gate, then roadmap. Depth is triaged, not maximal.
- **Supports agent-led execution** — agents can propose, build, verify, and bank while humans
  remain the escalation surface for irreversibles (`GATES.md`). Whether this reduces human work is
  an unverified hypothesis until the transplant and ablation phases complete.

## File map (every path below is verified by the checker)

| Path | What it is |
|---|---|
| `LAWS.md` | The eight proven laws, each with provenance and enforcement |
| `CLAIMS.md` | Falsifiable public claims, status, falsifier, and bound evidence |
| `AGENTS.md` | Universal worker contract — paste-portable to any harness |
| `GATES.md` | Human-key boundary + machine-parsed gate registry with SLA |
| `workflow/PLAN.md` | The living phased plan (the /phased format) |
| `workflow/canon/RETRACTIONS.md` | Ledger of numbers that are in the record but FALSE |
| `workflow/canon/DECISIONS.md` | Settled decisions — do not re-litigate |
| `workflow/templates/DISPATCH.md` | Schema for handing work to an agent |
| `workflow/templates/RECEIPT.md` | Schema for reporting work done |
| `workflow/templates/HANDOFF.md` | Cold-open session handoff memo format |
| `workflow/templates/EXPERIMENT.md` | Pre-registration + kill-bar template |
| `workflow/dispatches/` | Validated work claims; empty until a project needs one |
| `workflow/experiments/` | Validated experiment registrations; empty until a project needs one |
| `workflow/receipts/` | Banked receipts land here (linted) |
| `workflow/handoffs/` | Dated handoff memos land here |
| `scripts/onboard_check.py` | Verifies this documentation against reality |
| `scripts/sabotage_test.py` | Proves the checker fails on seeded defects |
| `scripts/status.py` | Computes phase status and verified-loop progress from artifacts |
| `scripts/checkpoint.py` | Refuses a git checkpoint while required checks are red |
| `scripts/transplant.py` | Non-destructively installs the invariant core into a clean target repo |
| `.github/workflows/verify.yml` | Runs both verification scripts in CI |
| `scripts/status.py` | Progress bars from the PLAN's phasing table + gate pressure |
| `scripts/checkpoint.py` | Verified snapshot: refuses to commit while checks are red |

## Onboarding a fresh harness (any vendor)

1. Run `python scripts/onboard_check.py` and `python scripts/sabotage_test.py`. Red means a claimed
   invariant or its refutation test is broken — fix that first.
2. Read `LAWS.md`, `AGENTS.md`, `GATES.md`, `workflow/PLAN.md`, and the newest file in
   `workflow/handoffs/` (if any). That is the complete state. Do not ask a human to re-explain.
3. Check `workflow/canon/RETRACTIONS.md` before citing ANY number found in older documents.
4. Claim work per `AGENTS.md`, do it, bank a receipt per the template, update the handoff.

## Transplanting SEED into a new project

Copy everything except `workflow/receipts/*` and `workflow/handoffs/*` contents. Rewrite the
four-line job and `workflow/PLAN.md` for the new problem. Open gate `G-001` (first commit) in
`GATES.md`. Run the checker. You are operational.

Last verified against reality: 2026-08-08.
