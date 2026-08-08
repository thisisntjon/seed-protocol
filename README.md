# SEED — a self-verifying operating skeleton for AI-driven projects

Drop these ~14 files into any project and any harness — Claude Code, Codex, Devin, whatever
comes next — can cold-onboard in minutes and operate with human intervention only at
irreversibles.

**Start at `START-HERE.md`. Trust nothing until `python scripts/onboard_check.py` is green.**

## What it encodes

Every rule here was earned by a documented incident in a year-long experiment (41 projects plus
a 30-day multi-agent campaign, audited 2026-08-08 by a twelve-agent investigation). The audit's
core finding: *implementation throughput is not an optimization gradient* — the scarce thing is
knowing whether work actually mattered. So the skeleton ships verification, not ceremony:

- **Machine-checked onboarding** — the docs are verified against reality; red means the docs lie.
- **Retraction ledger** — false numbers get a grave marker so they can't reinfect new sessions.
- **Gate SLA** — human-approval gates older than 48h fail the build, because "pending on the
  human" killed more origin-corpus projects than any bug.
- **Sabotage-tested guards** — `scripts/sabotage_test.py` proves the checker fails on the
  defects it claims to catch. A green guard without demonstrated refutation power is decorative.
- **Linted communication** — dispatch, receipt, handoff, and experiment schemas; "done" without
  evidence is not a state.

## Provenance

Distilled from: the Pokemon PTCG campaign's playbook and canon (`RULES-LEDGER`, `RETRACTIONS`,
`onboard_check` patterns), CAD v2.1 (protected oracles, budgeted-fix-then-revert), the BWA
build-it-twice experiment (3 -> 0 logic bugs under the framework), and the 2026-08-08 corpus
audit. Laws cite their incidents in `LAWS.md`.
