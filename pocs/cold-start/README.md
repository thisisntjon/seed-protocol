# Cold-start comprehension protocol

Purpose: measure whether repository state is sufficient for a fresh reader to recover the current
mission, authority boundary, experiment status, and next action without oral reconstruction.

1. Start from the exact `human-delta` commit named in `contract.json`.
2. Start a 15-minute timer before opening the repository.
3. Use repository evidence only. Do not receive a spoken summary or earlier conversation.
4. Record the exact commit, elapsed seconds, the eight declared choices, and evidence paths for
   each answer in the JSON shape used by `example-valid-v2.json`. The complete choice vocabulary
   is declared before the run; no hidden phrase is scored.
5. Run `python score-v2.py <answer.json>`. Contract source paths and git blob identities are frozen
   in `contract-v2.json` and can be checked with `verify-contract-v2.py`.

A PASS proves only that this reader recovered the frozen facts within the time ceiling. It does
not prove general portability, project effectiveness, or causal benefit. Bonkers P2 requires an
independent reader; the bundled examples are scorer calibration controls only. V1 remains
preserved as an invalid exact-token instrument.
