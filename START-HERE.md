# START HERE — machine-checked onboarding

**Rule of this file: it contains no sentence that a later sentence corrects. If reality changes,
this file is edited, not appended. `scripts/onboard_check.py` verifies its claims in CI.**

## THE WHOLE JOB, IN FOUR LINES

```
1. This repo is Bonkers. The BLUEPRINT is the factory for building other systems
   (workflow/blueprint/README.md). SEED is the protocol it contains.
2. Run python workflow/blueprint/bin/orient.py, then read LAWS.md, AGENTS.md, GATES.md.
   SEED workflow/PLAN.md is paused.
3. Run python scripts/onboard_check.py — it must pass before you act on anything written here.
4. Humans decide only what GATES.md lists. Everything else: proceed, leave receipts.
```

## Current effort (read this before the rest)

As of 2026-08-23 the active work is the **blueprint factory** at `workflow/blueprint/` —
an evolving system for building other systems (Miracle's suite pattern applied to
development). Start at `workflow/blueprint/README.md`. Architecture:
`workflow/blueprint/ARCHITECTURE.md`. It **supersedes SEED** as the product
(`workflow/canon/DECISIONS.md`, 2026-08-18); SEED remains the executable protocol in
this repo.

The harvest at `workflow/harvest/` feeds it: `workflow/harvest/IDEAS.md` (145 development ideas) and the
file pack. Cold start: `python workflow/blueprint/bin/orient.py`. Humans landing from GitHub
read `README.md` (research abstract); agents still start here.

What that means concretely for you:

- SEED's machinery in this repo still runs and is still authoritative for how work is done here:
  the laws, the gates, the receipts, the checkers. Keep using them.
- SEED's *roadmap* (`workflow/PLAN.md`, phases P1-P3) is paused. Do not resume P3 or any other
  SEED phase without a new decision; the blueprint's plan replaces it.
- The source material for the blueprint is the playbook directory of the poketcg repo
  (https://github.com/thisisntjon/poketcg) — 73 incident-earned rules — not this repo. This repo
  contributes whatever earns its place.
- A separate repo, thebus (https://github.com/thisisntjon/thebus), is RETIRED. It was an earlier
  attempt at fleet governance; its design is retracted and its research is banked there. Do not
  build on it.

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
| `README.md` | Research abstract for humans landing from GitHub |
| `CITATION.cff` | How to cite this repository and the case study |
| `LICENSE` | MIT |
| `CONTRIBUTING.md` | Research norms (pre-register, author XOR verifier) |
| `CLAIMS.md` | Falsifiable public claims, status, falsifier, and bound evidence |
| `AGENTS.md` | Universal worker contract — paste-portable to any harness |
| `GATES.md` | Human-key boundary + machine-parsed gate registry with SLA |
| `workflow/blueprint/ARCHITECTURE.md` | Factory architecture — current effort |
| `workflow/blueprint/README.md` | Factory front door (Miracle-style capability catalog) |
| `workflow/blueprint/CAPABILITY-CATALOG.md` | What ships, what is documented, what is deferred |
| `workflow/blueprint/EXTRACT-LOG.md` | File-by-file provenance of the extract |
| `workflow/blueprint/HARDENING.md` | Ten low-risk moves to lock recovered factory value |
| `workflow/research/2026-08-24-pr-case-study/PAPER.md` | Camera-ready PR case study (throughput ≠ progress) |
| `workflow/blueprint/PLAN.md` | Factory build plan (SEED PLAN.md is paused) |
| `workflow/blueprint/bin/orient.py` | Cold-start: SHA, four lines, stage, gates, next action |
| `workflow/blueprint/bin/bootstrap.py` | Install factory into a clean git repo |
| `workflow/blueprint/bin/selftest.py` | Catalog + ledger paths + orient sabotage |
| `workflow/PLAN.md` | SEED's phased plan (P1-P3), PAUSED as of 2026-08-18 |
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
| `scripts/poc_check.py` | Calibrates POC scorers against passing and expected-red controls |
| `scripts/poc_status.py` | Renders functionality progress from the ten-POC registry |
| `pocs/POC-REGISTRY.json` | Machine-readable status, evidence, and missing condition for ten POCs |
| `pocs/README.md` | POC ordering and truthfulness rules |
| `pocs/cold-start/` | Frozen truth contract and scorer for the 15-minute onboarding test |
| `pocs/deceptive-green/` | Source-vs-deployed-artifact false-green calibration fixture |
| `workflow/research/2026-08-08-poc-foundations.md` | Primary-source rationale for the POC architecture |
| `.github/workflows/verify.yml` | Onboard, sabotage, POC calibration, factory selftest, pack check, orient |
| `scripts/spend_check.py` | Law 9: fails when compute burns without closed loops |
| `scripts/stress_test.py` | Randomized defect-injection stress test of the guards at scale |
| `workflow/harvest/PLAN.md` | Harvest phased plan — feeds the blueprint |
| `workflow/harvest/IDEAS.md` | Development ideas earned in the origin campaign — the growing factory ledger |
| `workflow/harvest/INVENTORY.md` | Classified *files* (CORE / OPTIONAL / NEVER) — how some ideas are already encoded |
| `workflow/harvest/pack/README.md` | How to install CORE, identity templates, and optional extras |
| `workflow/harvest/pack/assemble.py` | Validate the pack; materialize it into a clean git repo |

## Onboarding a fresh harness (any vendor)

1. Run `python scripts/onboard_check.py`, `python scripts/sabotage_test.py`, and
   `python scripts/poc_check.py`. Red means a claimed
   invariant or its refutation test is broken — fix that first.
2. Run `python workflow/blueprint/bin/orient.py`, then read `workflow/blueprint/README.md`,
   `LAWS.md`, `AGENTS.md`, `GATES.md`, `workflow/blueprint/PLAN.md`, and the newest file in
   `workflow/handoffs/` (if any). SEED's `workflow/PLAN.md` is paused. Do not ask a human
   to re-explain.
3. Check `workflow/canon/RETRACTIONS.md` before citing ANY number found in older documents.
4. Claim work per `AGENTS.md`, do it, bank a receipt per the template, update the handoff.

## Transplanting SEED into a new project (interim; the blueprint replaces this)

Copy everything except `workflow/receipts/*` and `workflow/handoffs/*` contents. Rewrite the
four-line job and `workflow/PLAN.md` for the new problem. Open gate `G-001` (first commit) in
`GATES.md`. Run the checker. You are operational.

Last verified against reality: 2026-08-31.

