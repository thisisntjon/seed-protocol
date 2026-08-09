# LAWS — the rules the experiment actually proved

Format follows the RULES-LEDGER pattern: every law names the evidence that earned it and how it
is enforced. Enforcement grades: **ENCODED** (a machine check fails without it), **CHANNEL**
(the structure makes violation impossible), **PROSE** (words only — the weakest grade; the origin
corpus found every prose rule was eventually violated, so PROSE laws are debts awaiting encoding).

**Scope rule (meta-law):** an addition to this skeleton requires a named incident that earned it.
No speculative structure. The origin corpus's 646-tool sprawl is the anti-pattern.

---

## Law 1 — Encoded beats prose
Every rule that matters becomes a machine check or a structural constraint. Incidents may add a
check, never a paragraph.
**Earned by:** playbook/RULES-LEDGER.md finding — "every encoded rule never failed again; every
prose rule was violated at least once."
**Enforcement:** ENCODED — this skeleton ships `scripts/onboard_check.py`; laws without a check
are marked PROSE below as visible debt.

## Law 2 — Sabotage before trust
A guard is not trusted until it demonstrably fails on the defect it claims to catch. Ask of every
check: "would it produce the same output if the thing it describes were completely broken?"
**Earned by:** six documented instrument failures in the Pokemon campaign, incl. `PREFLIGHT
PASSED` with 14/23 checks silently skipped, and ~290,000 games measuring a module the live
policy never imported.
**Enforcement:** ENCODED — `scripts/sabotage_test.py` seeds four defect classes and requires the
checker to fail on each.

## Law 3 — Measure the deployed artifact, not the repo
Verification runs against the packed/shipped object under the target runtime. A local result
about one object is not evidence about a differently packaged object. Identity is by hash,
never by label or filename.
**Earned by:** Kaggle submissions silently playing worse-than-random fallback while local evals
looked fine (EVAL_PROTOCOL E016/E022); 133 deck files collapsing to 26 distinct lists.
**Enforcement:** PROSE (debt) — encode a deployment-parity preflight per project; the skeleton
cannot know your runtime. `workflow/templates/EXPERIMENT.md` forces an artifact-hash field.

## Law 4 — Pre-register, then honor the kill bar
Success and kill criteria are committed to git BEFORE results exist. A screen that dies at power
is not shipped, no matter how coherent its narrative. Positives need independent (non-author)
reproduction; negatives bank same-day author-only.
**Earned by:** the +0.592pp SETUP_GREED mirage (reversed to −0.154pp at 2.6× sample, not
shipped); seq-808 killing the team's own hoped-for silver shot at 23.42% vs a pre-stated <35% bar.
**Enforcement:** CHANNEL — `workflow/templates/EXPERIMENT.md` has no free-text verdict; outcomes
are one of PASS / KILL / NULL / INVALID-INSTRUMENT, pre-registered by commit.

## Law 5 — State lives in artifacts
Chat is ephemeral; heads are lossy. Plans, decisions, receipts, retractions, and handoffs live in
files a cold session can read. The health metric: each successive handoff memo gets shorter.
**Earned by:** the Pokemon repo surviving fleet-wide session death repeatedly; "picking this back
up costs an hour, not a week."
**Enforcement:** CHANNEL + ENCODED — templates exist for every artifact type; the checker validates
receipt, dispatch, experiment, and handoff instances and verifies every concrete path this
documentation claims.

## Law 6 — Correct by editing, retract by ledger
Append-only correction means the wrong answer sits above the right one and grep finds it first.
`START-HERE.md` is edited in place; numbers that were published and are now known false go in
`workflow/canon/RETRACTIONS.md` with what to use instead. Check the ledger before citing any
number from an older document. Patch the generator, not the output.
**Earned by:** 66 files still citing a retracted figure in the origin corpus; "the announcement
of the replacement could not travel through the channel that had just failed."
**Enforcement:** ENCODED — the checker fails if a retracted token is cited outside the ledger.

## Law 7 — Humans gate irreversibles only, and gates carry an SLA
Agents research, build, and verify without asking. Humans decide only what `GATES.md` lists:
spend, publication, deletion, submission, production flips. BUT: a gate pending past its SLA is
an incident, surfaced loudly — because "waiting on the human" is the #1 documented project killer.
**Earned by:** TheHolyGrail (died at "register the GitHub App"), The Village ("GATE PENDING
(Jon)", dormant for a month) — the methodology's safety feature was also its abandonment vector.
**Enforcement:** ENCODED — `GATES.md` carries a machine-parsed registry; the checker fails on any
OPEN gate older than its SLA.

## Law 8 — Throughput is not progress; verify, then ablate
Commits, PRs, tools, and documents are activity metrics. Progress is a closed loop: hypothesis →
pre-registered test → verified result → decision. Periodically ablate the harness itself: re-test
whether each component still earns its keep on current models, and delete what doesn't. Default
to ONE strong agent; add parallel workers only for provably independent, worktree-isolatable work.
**Earned by:** 2,199 PRs coexisting with zero closed experiment loops for 24 days; 30 days of
max-throughput fleet work producing zero confirmed improvements; 2026 public evidence (multi-agent
~3× tokens, up to −70% on interdependent tasks).
**Enforcement:** PROSE (debt) — P3 of `workflow/PLAN.md` schedules the first ablation; encode a
recurring one per project.

## Law 9 — Spend buys closed loops, and it is always metered
Compute consumption is measured on a cadence (a stale meter is itself a failure), every window
of spend must name the loops it closed, and every dispatch carries a FORECAST that its receipt's
ACTUAL grades. Spend above threshold with zero closed loops fails the build. Dollar figures
derived from token counts are always labeled API-LIST-EQUIVALENT, never presented as cash.
**Earned by:** the 2026-08-08 metering of the origin corpus — ~$49,686 API-list-equivalent
consumed across the surviving transcript window while the campaign's own verdict was "zero
confirmed agent improvements", and playbook/COST.md's spend table was empty checkboxes: an
evidence culture that demanded receipts for everything exempted its own cost from evidence.
**Enforcement:** ENCODED — `scripts/spend_check.py` (fails on unmetered, stale, or loop-less
spend; selftest proves refutation power) + FORECAST required on dispatches and SESSION_ID on
new receipts by `scripts/onboard_check.py`.
