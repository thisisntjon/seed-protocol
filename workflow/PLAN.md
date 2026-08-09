# SEED — Skeleton Framework Plan (Living Document)

Format: phased-investigation-workflow (`/phased`).
Triage depth: **Medium** — the investigation stage was satisfied by the 2026-08-08 twelve-agent
corpus audit (see Research); this plan records its synthesis and governs the build.
Current stage: phase P3 — plan gate for matched-ablation instrumentation
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

- Assumption: A credible autonomy thermometer must separate task, solver, deployed artifact,
  protected scorer, and human intervention record; an agent's own completion claim is not an
  outcome.
  Source: UK AISI Inspect component model + SWE-bench-Live executable environments + Pokemon
  false-green incidents; `workflow/research/2026-08-08-poc-foundations.md`
  Status: holding — instrument calibration implemented; prospective runs pending
  | Affects: P2 cold onboarding, P3 ablation, Human Delta pilot schema

- Assumption: Success should be reported against expert-human task time and total expenditure
  (human time, tokens, and experiment compute), not throughput alone.
  Source: METR time horizon and expenditure horizon; MLE-bench human leaderboard baselines;
  `workflow/research/2026-08-08-poc-foundations.md`
  Status: holding — adopted as measurement design; no Human Delta curve measured yet
  | Affects: P3 endpoints and later public thermometer

- Assumption: Exact-token equality is a valid protected scorer for semantic cold-onboarding
  comprehension when the response schema asks only for "short uppercase semantic codes."
  Source: POC-01 v1 scorer and first independent run at Human Delta
  Status: invalidated (2026-08-08) — the reader recovered the correct mission, authority boundary,
  phase, next action, both invalid experiments, pending P2c state, and unsupported causal claim in
  95 seconds, but synonymous codes match only 3/8 frozen strings. The scorer confounds vocabulary
  with comprehension.
  | Affects: P2 cold-onboarding gate, POC-01, and the scoring architecture for P3

- Assumption: A fact-specific evidence allowlist can remain hidden from the reader without
  confounding evidentiary quality with path choice.
  Source: POC-01 v2 contract and second independent run at Human Delta
  Status: invalidated (2026-08-08) — the reader selected 8/8 correct declared facts and cited the
  direct P2b experiment plus its terminal receipt, but the scorer awarded 7/8 evidence because its
  hidden allowlist accepted only START-HERE.md or workflow/PLAN.md for P2b.
  | Affects: P2 cold-onboarding gate, POC-01, and evidence scoring for P3

- Assumption: The P3 treatment identity `e46361e...` remains a valid SEED object.
  Source: original P3 preregistration
  Status: invalidated (2026-08-08) — P2a killed this identity because its portable manifest omitted
  a runtime dependency required by its own sabotage suite. The recommended replacement is the
  P2c-proven `bed1e9e...`; the current `7f4cebdb...` is a later replication candidate.
  | Affects: P3 treatment, preregistration, and every downstream causal claim

- Assumption: Live human-intervention minutes can be captured prospectively without material
  missingness or observer effect.
  Source: P3 secondary endpoint and POC-08 design
  Status: unverified — build and sabotage-test the event logger before any registered solver run
  | Affects: P3 human-cost endpoint and public Human Delta thermometer

- Assumption: Twelve binary matched pairs support the preregistered 25pp directional claim.
  Source: P3 fixed sample
  Status: unverified — the original “paired 90% interval” does not name an estimator. Proposed exact
  rule is mean paired effect >=25pp plus one-sided discordant-pair p<=0.10; at n=12 the smallest
  simple pass is four discordant pairs all favoring SEED.
  | Affects: P3 PASS interpretation and POC-09

## Phasing

<!-- Status column machine-parsed by scripts/status.py: DONE | ACTIVE | ACTIVE(nn%) | TODO -->

| Phase | Scope | Gate | Status |
|---|---|---|---|
| P1 Skeleton | All files + working checks + progress/checkpointing | onboard_check green; sabotage_test proves red-on-defect | DONE |
| P2 First transplant | Drop skeleton into one real new project | fresh session onboards ≤15 min from START-HERE alone | DONE |
| P3 Ablation | Compare SEED vs. bare instructions across twelve matched task pairs | blinded fixed-sample terminal, including an honest null | ACTIVE(20%) |
| P4 External proof | A second user/machine runs SEED; skeleton published after the Sept 13 fence lifts | one adoption or review by someone who is not Jon | TODO |

## Phase Log

### Pivot — 2026-08-08 — P3 treatment identity is dead

P3's registered `e46361e...` object was subsequently killed by P2a, so executing it would measure a
known-broken package. The causal question survives. The recommended local pivot is to freeze the
P2c-proven identity `bed1e9e...` from source `728ff959...` as the first P3 treatment and defer the
current `7f4cebdb...` identity to a later replication. Investigation also found two prerequisites
that must precede spend: prospective human-intervention capture (POC-08) and an exact small-sample
test replacing the under-specified “paired 90% interval.” The twelve-pair sample and roadmap remain
unchanged. Execution is held at the plan gate; no solver/model run is authorized by this pivot.
Research: `workflow/research/phase-P3-ablation-design.md`. Phase plan: `workflow/phases/P3.md`.

### Pivot — 2026-08-08 — cold-onboarding scorer is lexically invalid

The first independent reader returned the correct substantive state at exact Human Delta commit
`2ff86b5` in 95 seconds and independently identified a stale PLAN-header contradiction. The frozen
v1 scorer rejects the run because five semantically equivalent uppercase codes do not equal its
hidden canonical strings. The run is preserved as INVALID-INSTRUMENT; it is neither retrofitted to
PASS nor treated as a failure to onboard. Blast radius is local to scoring: the transplant bytes,
15-minute endpoint, and P3 causal protocol remain intact. Jon approved the pivot. Replace hidden
exact-token scoring with a source-bound declared-choice rubric that requires evidence paths,
preregister v2, then run a new independent reader. Do not reuse the v1 reader for the v2 terminal.
Roadmap sequencing is unchanged because the failure is local to the scoring instrument.

### Pivot — 2026-08-08 — v2 evidence allowlist is under-scoped

V2 repaired hidden vocabulary but repeated the same class at the evidence layer. A new reader
returned the exact target, 8/8 correct declared facts, and evidence for every field in 70 seconds.
The scorer rejected P2b only because the reader cited the specific experiment and terminal receipt
instead of two hidden summary paths. Preserve v2 as INVALID-INSTRUMENT. Jon approved v3: validate
any safe cited path that exists at the exact target commit against
preregistered fact anchors. Use a new reader; do not retrofit or reuse the v2 result. Roadmap
sequencing remains unchanged because the failure remains local to the scoring instrument.

### P2 close — 2026-08-08 — first transplant and cold onboarding PASS

V3 closed the gate at exact Human Delta commit `2ff86b5`: target commit available, identity PASS,
75/900 seconds, 8/8 facts, 8/8 content-validated evidence, zero clarifications, and zero target
writes. P2a, P2b, scorer v1, and scorer v2 remain preserved negative terminals; no result was
rescued. C-003 advances only for the tested second-project transplant. C-004 causal benefit stays
HYPOTHESIS and moves to P3's fixed matched ablation. P2 is DONE; P3 begins in investigation.

- 2026-08-08 — P2 instrument calibration designed from primary sources and implemented without
  altering the frozen P3 causal protocol. The cold-start scorer binds answers to Human Delta's
  exact commit and 15-minute ceiling; the deceptive-green fixture proves a source-tree check can
  pass while the deployable artifact fails. These are controls, not evidence of SEED benefit;
  P2c still requires an independent cold run. Calibration terminal:
  `workflow/receipts/2026-08-08-poc-instrument-calibration.md` at `9cec215` (10/10 controls).
- 2026-08-08 — P2c local gates passed at `human-delta@9703c52`: existing tests 8/8,
  sabotage 18/18, onboard 0 errors, source import scan clean, and no target-owned overwrite.
  Independent cold onboarding remains load-bearing; portability claim C-003 stays HYPOTHESIS.
- 2026-08-08 — P2a terminated INVALID-INSTRUMENT at exact target commit `human-delta@e972da4`:
  the portable manifest omitted a runtime dependency of its own sabotage suite. The failure is
  preserved; P2b must use a new identity and registration. This is the first evidence supporting
  C-005 (negative results remain terminal rather than being narratively rescued).
- 2026-08-08 — P2b preregistered against new portable identity `7114e2e...`. The upgrade path
  may replace only bytes matching P2a provenance; target-modified bytes remain hard conflicts.
- 2026-08-08 — P2b terminated INVALID-INSTRUMENT at `human-delta@ce8aa4b`: its retraction
  sabotage assumed a Bonkers-only example token and therefore stayed green against Human Delta's
  valid empty ledger. P2c must seed both the retraction and its forbidden citation inside the
  disposable target.
- 2026-08-08 — P2c preregistered against portable identity `bed1e9e...`; it changes only the
  provenance-matched sabotage file and seeds its own disposable retraction fixture.
- 2026-08-08 — P2 and P3 preregistered before transplant results. Exact source was amended before
  execution to `e08c365` to include the conflict-refusing transplant tool;
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

- P3 ablation design and pivot: `workflow/research/phase-P3-ablation-design.md`
- P3 gated execution plan: `workflow/phases/P3.md`

- Corpus audit report (primary): https://claude.ai/code/artifact/a82abedd-c7de-4407-9a4c-b9e5bfb1cf86
- Origin exemplars: `Desktop\Pokemon\START-HERE.md` + `scripts\onboard_check.py` (machine-checked
  onboarding), `Desktop\Pokemon\playbook\` (portable factory), `Desktop\Pokemon\workflow\canon\RETRACTIONS.md`
  (retraction ledger), `Desktop\Python\CAD-v2.1-final.md` (protected oracles, budgeted-fix-then-revert),
  `Desktop\Python\BWA\archive\LEARNINGS-REPORT.md` (the controlled A/B experiment).
