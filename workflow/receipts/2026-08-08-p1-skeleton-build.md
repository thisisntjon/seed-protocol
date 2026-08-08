STATE:       DONE
OBJECT:      P1 of workflow/PLAN.md -- the skeleton itself (14 files + working checks)
EXACT_REF:   pre-first-commit working tree of 2026-08-08 (gate G-001 open)
EVIDENCE:    `python scripts/onboard_check.py` -> 0 error(s), ONBOARD CHECK PASSED;
             `python scripts/sabotage_test.py` -> 5/5 PASS (clean green; missing-path,
             stale-gate, evidence-less-receipt, retracted-citation all red as required)
NEXT_OWNER:  gate G-001 (human: initial commit), then P2 (first transplant into a real project)
