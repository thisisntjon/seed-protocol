STATE:       DONE
OBJECT:      Calibrate POC-01 cold-start comprehension and POC-02 deceptive-green detection.
EXACT_REF:   9cec215ec4013b4fe0045df5f197c591a9747217
EVIDENCE:    `python scripts/poc_check.py` returned 10/10 PASS at the exact ref; `python scripts/onboard_check.py` returned 0 errors; `python scripts/sabotage_test.py` returned 18/18 PASS. Research and design rationale are bound in `workflow/research/2026-08-08-poc-foundations.md`.
PROGRESS:    MEASUREMENT
EFFECT:      The cold-start scorer rejects false facts, stale identity, and >900-second runs; the protected artifact scorer reproduces a weak-check-green/deployed-artifact-red failure. This validates the instruments only and does not support causal benefit.
BLOCKED_ON:  none
NEXT_OWNER:  Bonkers P2 gate — consume the cold-start scorer in an independent run; keep P3 causal claims pending.
