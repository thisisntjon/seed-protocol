# SEED — Skeleton Framework Plan (Living Document)

Format: phased-investigation-workflow (`/phased`).
Triage depth: **Medium** — the investigation stage was satisfied by the 2026-08-08 twelve-agent
corpus audit (see Research); this plan records its synthesis and governs the build.
Current stage: roadmap -> executing P2 first transplant
Last updated: 2026-08-08

## Problem

**Problem:** Every new project re-derives its operating system from scratch. Onboarding a fresh
harness (Claude Code, Codex, Devin, any future agent) into an existing effort costs hours of
re-discovery, and the corpus's own record shows the failure modes that follow: docs drift,
retracted numbers get re-cited, gates silently die waiting on a human, and throughput substitutes
for verified progress.

**Why now:** The 2026-08-08 audit distilled a year of evidence (41 projects + a 30-day fleet
campaign) into a small set of proven laws. That knowledge is currently spread across two
directories and one report. Compounding only happens if it becomes a drop-in skeleton.

**Hypothesis:** A small, incident-bounded protocol — where enforcement strength is explicit and
important claims have refutation tests — lets a capable agent cold-onboard in ≤15 minutes and
helps a project run research → build → verify while reserving irreversible decisions for humans.

## Goal

A copyable skeleton (this repo) that a fresh harness can onboard into from `START-HERE.md` alone,
that machine-verifies its own documentation, that surfaces dying human gates before they kill the
project, and that carries the communication schemas (dispatch/receipt/handoff) proven in the
Pokemon campaign.

## Success Criteria

1. `python scripts/onboard_check.py` passes clean on this repo. 
2. `python scripts/sabotage_test.py` proves the checker FAILS on each seeded defect class
   (missing path, overdue/invalid gates, malformed artifact schemas, and retracted-value
   citations anywhere in the project) — a guard is not
   trusted until it fails on the defect it claims to catch. 
3. Every law in `LAWS.md` cites the incident/evidence that earned it and names its enforcement
   (ENCODED / CHANNEL / PROSE), with PROSE kept to a minimum. 
4. The portable core copies into a new project with only explicitly documented project-specific
   fields rewritten.
5. A cold session can state the whole job from the first four lines of `START-HERE.md`. 

## Assumption Registry

- Assumption: One strong agent with locked acceptance criteria outperforms a fleet on
  interdependent work; fleet layering is opt-in, not default.
  Source: Pokemon campaign result (zero confirmed improvements at max fleet throughput) +
  2026 public evidence (multi-agent ~3x tokens, up to -70% on interdependent tasks)
  Status: holding
  | Affects: AGENTS.md default operating mode

- Assumption: The gate-SLA check (surface any OPEN human gate older than 48h) prevents the
  corpus's #1 project-death mode (TheHolyGrail, The Village both died at "pending Jon").
  Source: 2026-08-08 audit, skeptic finding
  Status: unverified — this skeleton is the first implementation
  | Affects: GATES.md + onboard_check.py

- Assumption: Encoded rules do not fail again; prose rules get violated.
  Source: playbook/RULES-LEDGER.md empirical claim, Pokemon campaign
  Status: verified in origin corpus; carried as design principle here
  | Affects: everything — checks over prose throughout

- Assumption: A small, incident-bounded core is the right shape; the 646-tool sprawl of the origin
  corpus is the anti-pattern ("the valuable core is 8-12 components" — Sol assessment).
  Source: PTCG_SOL_VALUE_ASSESSMENT_2026-08-08.md
  Status: holding
  | Affects: scope — additions require a named incident, per Law 6

## Phasing

<!-- Status column machine-parsed by scripts/status.py: DONE | ACTIVE | ACTIVE(nn%) | TODO -->

| Phase | Scope | Gate | Status |
|---|---|---|---|
| P1 Skeleton | All files + working checks + progress/checkpointing | onboard_check green; sabotage_test proves red-on-defect | DONE |
| P2 First transplant | Drop skeleton into one real new project | fresh session onboards ≤15 min from START-HERE alone | ACTIVE(20%) |
| P3 Ablation | Compare a skeleton-run project vs. bare-harness on one comparable task | measured delta recorded here, whatever it shows | TODO |
| P4 External proof | A second user/machine runs SEED; skeleton published after the Sept 13 fence lifts | one adoption or review by someone who is not Jon | TODO |

## Phase Log

- 2026-08-08 — P2 and P3 preregistered before transplant results. Exact source is `d609ef9`;
  exact Human Delta baseline is `04da0ca`. P2 may establish portability only; it cannot establish
  causal benefit. P3 is the first design capable of supporting or refuting the benefit claim.
- 2026-08-08 — Verified-progress control closed: status reports one decision/measurement loop,
  one infrastructure completion, and one invalidated receipt after the encoded behavioral test.
  This supports only the accounting property, not project effectiveness.
- 2026-08-08 — P1 truthfulness hardening DONE at `1e5bc7d`: onboard check 0 errors;
  sabotage test 10/10; schema instances, gate states, project-wide Markdown retractions, law
  evidence/enforcement, CI, status, and checkpoint paths verified. Replacement receipt:
  `workflow/receipts/2026-08-08-p1-truthfulness-hardening.md`. P2 is now the critical path.
- 2026-08-08 — P1 truthfulness-hardening increment locked against baseline `3730a79` after
  review found three contradictions: no reproducible git identity, schema-lint claims wider than
  implementation, and a stale-gate sabotage coupled to the presence of an existing OPEN gate.
  Acceptance: strict gate/status validation; project-wide Markdown retraction scan; structured
  receipt/dispatch/experiment/handoff validation; CI entrypoint; independent sabotage for every
  added check; clean status/checkpoint path; banked receipt bound to the resulting commit.
- 2026-08-08 — Evidence-portability debt recorded: the primary corpus audit currently resolves to
  an external artifact rather than a repository-bound evidence pack. P2 may cite it as context,
  but cannot treat its universal claims as independently reproducible until exported or rebuilt.
- 2026-08-08 — Investigation satisfied by the twelve-agent corpus audit (8 local readers, 3 web
  researchers, 1 adversarial skeptic). Report:
  https://claude.ai/code/artifact/a82abedd-c7de-4407-9a4c-b9e5bfb1cf86
- 2026-08-08 — Synthesis: the durable value is the verification/orchestration methodology;
  this skeleton is its extraction. Roadmap approved implicitly by the build directive. P1 started.

## Research

- Corpus audit report (primary): https://claude.ai/code/artifact/a82abedd-c7de-4407-9a4c-b9e5bfb1cf86
- Origin exemplars: `Desktop\Pokemon\START-HERE.md` + `scripts\onboard_check.py` (machine-checked
  onboarding), `Desktop\Pokemon\playbook\` (portable factory), `Desktop\Pokemon\workflow\canon\RETRACTIONS.md`
  (retraction ledger), `Desktop\Python\CAD-v2.1-final.md` (protected oracles, budgeted-fix-then-revert),
  `Desktop\Python\BWA\archive\LEARNINGS-REPORT.md` (the controlled A/B experiment).
