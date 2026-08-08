# Bonkers / SEED — an epistemic control plane for AI-driven projects

**Bonkers** is the project. **SEED** is the small, portable protocol it contains.

SEED is designed to help a capable coding agent cold-onboard, preserve trustworthy state, expose
false progress, and escalate only irreversible decisions. It is not an agent runtime, scheduler,
or proof of autonomy; those claims require the transplant and ablation phases in
`workflow/PLAN.md`.

**Start at `START-HERE.md`. Trust nothing until `python scripts/onboard_check.py` is green.**

## What it encodes

Every rule here was earned by a documented incident in a year-long experiment (41 projects plus
a 30-day multi-agent campaign, audited 2026-08-08 by a twelve-agent investigation). The audit's
core finding: *implementation throughput is not an optimization gradient* — the scarce thing is
knowing whether work actually mattered. So the skeleton ships verification, not ceremony:

- **Machine-checked onboarding** — concrete documentation, workflow artifacts, gates, and
  retractions are checked against the repository; red identifies a known contradiction class.
- **Retraction ledger** — false numbers get a grave marker so they can't reinfect new sessions.
- **Gate SLA** — human-approval gates older than 48h fail the build, because "pending on the
  human" killed more origin-corpus projects than any bug.
- **Sabotage-tested guards** — `scripts/sabotage_test.py` proves the checker fails on the
  defects it claims to catch. A green guard without demonstrated refutation power is decorative.
- **Linted communication** — dispatch, receipt, handoff, and experiment instances are validated;
  "done" without evidence is not a state.

The checker proves only its named checks. `scripts/sabotage_test.py` exists to demonstrate that
each claimed defect class can actually turn the repository red.

## Provenance

Distilled from: the Pokemon PTCG campaign's playbook and canon (`RULES-LEDGER`, `RETRACTIONS`,
`onboard_check` patterns), CAD v2.1 (protected oracles, budgeted-fix-then-revert), the BWA
build-it-twice experiment (3 -> 0 logic bugs under the framework), and the 2026-08-08 corpus
audit. Laws cite their incidents in `LAWS.md`.
