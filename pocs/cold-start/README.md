# Cold-start comprehension protocol

Purpose: measure whether repository state is sufficient for a fresh reader to recover the current
mission, authority boundary, experiment status, and next action without oral reconstruction.

1. Start from the exact `human-delta` commit named in `contract.json`.
2. Start a 15-minute timer before opening the repository.
3. Use repository evidence only. Do not receive a spoken summary or earlier conversation.
4. Record the exact commit, elapsed seconds, and the eight enumerated answers in the JSON shape
   used by `example-valid.json`.
5. Run `python score.py <answer.json>`.

A PASS proves only that this reader recovered the frozen facts within the time ceiling. It does
not prove general portability, project effectiveness, or causal benefit. Bonkers P2 requires an
independent reader; the bundled examples are scorer calibration controls only.
