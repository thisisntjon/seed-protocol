# FRONT-DOOR — first 90 seconds (T-001)

Proposal only. Does not edit `README.md`. Does not flip visibility
(`GATES.md` item 2, publication). No new SUPPORTED rows.

## Identity

**First sentence a stranger can repeat:**

> Bonkers is a measurement protocol called SEED; the GitHub name thefleet is historical, and fleet orchestration is deferred.

| Name | Public role |
|---|---|
| **Bonkers** | The project. Lead with this. |
| **SEED** | The protocol (claims C-001–C-005). |
| **thefleet** | GitHub slug only. Do not rename in this ticket; use a subtitle. |
| **fleet** | Deferred. Default is one strong agent (`CONTRIBUTING.md`; DECISIONS 2026-08-08). |

Recommended display subtitle (not a rename): `Bonkers / SEED`.

## Clock (clone → 90s)

| t | What they see |
|---|---|
| 0–15s | H1 + first sentence. Identity tax is gone. |
| 15–35s | Abstract, then research question. C-004 named as **HYPOTHESIS**. |
| 35–55s | **Limitations** — before any capability, factory, or harvest list. |
| 55–75s | `JUDGES.md`: score the instrument, not treatment effect. |
| 75–90s | One reproduce line: `python scripts/onboard_check.py`. Green docs ≠ answered question. |

Do not open with a product landing page, a fleet pitch, or a capabilities tour.

## GitHub About (description)

One-liner (≤350 characters):

> Bonkers (SEED): a measurement protocol for agentic software work — not a fleet.

Topics (if set later): `research`, `reproducibility`, `agents`, `evaluation`.
Website: none unless a human gates a publication URL.

## README H2 outline

Lead abstract → question → limitations **before** capabilities.

1. **Abstract** — first sentence, then: epistemic control plane; does not schedule agents.
2. **Research question** — registered as C-004; status **HYPOTHESIS**; null is valid.
3. **Limitations** — instrument ≠ benefit; case study n=1 author-run; playbook recurrence unverified; factory bootstrap not a CI fixture; visibility flip is a gate.
4. **Claim status** — existing table only (C-001–C-005). Do not add rows.
5. **Evidence in this tree** — pinned case study + `artifacts/`; instrument calibration under `pocs/`.
6. **Reproduce** — onboard / sabotage / poc / factory selftest. One figure later (T-003), not here.
7. **How to read the tree** — `CLAIMS.md`, experiments, receipts, retractions.
8. **Related work** — merge-rate papers answer acceptance; this tree asks composition.
9. **Cite** — `CITATION.cff`; author-run caveat attached.
10. **License** — MIT.
11. **Contributing** — research norms; fleet opt-in.

Capabilities (factory extract, harvest ledger, transplant) may appear only after §3, and only as *what the instrument contains*, not as proof it helps.

## JUDGES.md outline

Purpose: this entry is **the instrument**, not C-004. C-004 stays **HYPOTHESIS**.

Proposed H2s:

1. **Score this as an instrument** — can a stranger name it, run the checker, and see claim status? A treatment-effect score is the wrong rubric.
2. **Registered question** — C-004 (false progress / recovery / human load vs bare). Status: HYPOTHESIS. Ablation designed and paused. Do not infer it from a green CI or a polished README.
3. **What a high score means** — falsifiers exist; sabotage suite is runnable; supported rows match bound receipts; a negative result can be published (C-005).
4. **What a high score does not mean** — SEED is not shown to outperform a bare repo. The poketcg census is composition and identity, not a causal estimate.
5. **90-second path** — this file → README §§Abstract–Limitations → `CLAIMS.md` → `python scripts/onboard_check.py`.
6. **Author XOR verifier** — the session that writes a positive claim does not grade it (`CONTRIBUTING.md`).
7. **Kill / null / invalid-instrument** — the only legal empirical outcomes. Rescue-as-success is a C-005 fail.

Assumption (holding, PLAN): a mixed panel can approach a high score only if the entry is graded as the instrument.

## Must not be claimed

- That using SEED improves outcomes versus bare (that is C-004; **HYPOTHESIS**).
- That this is an agent runtime, orchestrator, or autonomy demo.
- That the GitHub name implies a working multi-agent fleet.
- That the PR case study is a treatment effect, a merge-rate result, or independently reproduced.
- That “encoded rules never failed again” is measured (`DECISIONS.md` caveat).
- That a green onboard check answers the research question.
- That a private remote, or a private backup, is public publication.
- Any new SUPPORTED row, or any upgrade of C-004 by repetition or README polish.
- Replacement-cost or unverified Law-9 dollars (hygiene is T-002).

## Fence for T-006

Implement README / `JUDGES.md` / About on a later board. This brief locks identity, section order, and the scoring frame. Out of scope here: CI, bootstrap, VoiceCraft, fleet mailbox, repo rename, visibility flip.
