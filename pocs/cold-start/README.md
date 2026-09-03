# Cold-start comprehension protocol

Purpose: measure whether repository state is sufficient for a fresh reader to recover the current
mission, authority boundary, experiment status, and next action without oral reconstruction.

1. Start from the exact `human-delta` commit named in `contract.json`.
2. Start a 15-minute timer before opening the repository.
3. Use repository evidence only. Do not receive a spoken summary or earlier conversation.
4. Record the exact commit, elapsed seconds, the eight declared choices, and evidence paths for
   each answer in the JSON shape used by `example-valid-v2.json`. The complete choice vocabulary
   is declared before the run; no hidden phrase is scored.
5. Run `python score-v3.py <answer.json> --target-repo <target>`. V3 accepts any safe cited path
   that exists at the exact commit and validates its contents against frozen fact anchors; it has
   no hidden evidence-path allowlist.

A PASS proves only that this reader recovered the frozen facts within the time ceiling. It does
not prove general portability, project effectiveness, or causal benefit. SEED P2 requires an
independent reader; the bundled examples are scorer calibration controls only. V1 remains
preserved as an invalid exact-token instrument, and V2 as an invalid hidden-path instrument.
