# JUDGES — score the instrument

This entry is **Bonkers / SEED**, a measurement protocol. The GitHub slug
`thefleet` is historical. Fleet orchestration is deferred.

Do not score treatment effect. C-004 stays **HYPOTHESIS**.

## Score this as an instrument

A high score means a stranger can name the object, run the checker, and see
claim status without being sold a fleet or a causal win. Ask:

- Can they repeat the first sentence of [`README.md`](README.md)?
- Does `python scripts/onboard_check.py` exit 0, and do they know green docs
  are not an answered research question?
- Do supported rows in [`CLAIMS.md`](CLAIMS.md) match bound receipts?

A rubric that grades “does SEED beat a bare repo?” is the wrong rubric.

## Registered question

Does an incident-earned, machine-checked control plane reduce invalid
completion claims, recovery cost, or unnecessary human intervention relative
to a bare repository, without a material drop in correct task completion?

Registered as **C-004**. Status: **HYPOTHESIS**. The matched ablation is
designed and paused
(`workflow/experiments/2026-08-08-p3-bare-vs-seed-ablation.md`). A null
result is a valid outcome. Do not infer C-004 from a green CI run or a
polished README.

## What a high score means

- Falsifiers exist on every public claim.
- The sabotage suite is runnable (`python scripts/sabotage_test.py`).
- Supported rows match bound evidence in this tree.
- A negative result can be published without being rewritten as success
  (C-005).

## What a high score does not mean

- SEED is not shown to outperform a bare repo.
- The poketcg census is composition and identity, not a causal estimate and
  not independently reproduced. The public dataset is
  [`workflow/research/2026-08-24-pr-case-study/artifacts/`](workflow/research/2026-08-24-pr-case-study/artifacts/).
  The clone that produced it is not this repository.
- This is not an agent runtime, orchestrator, or autonomy demo.
- A green onboard check does not answer the research question.

## 90-second path

1. This file.
2. [`README.md`](README.md) Abstract through Limitations.
3. [`CLAIMS.md`](CLAIMS.md).
4. `python scripts/onboard_check.py`.

## Author XOR verifier

The session that writes a positive claim does not grade it. See
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Kill / null / invalid-instrument

The only legal empirical outcomes are PASS, KILL, NULL, and
INVALID-INSTRUMENT. Rescue-as-success is a C-005 fail.
