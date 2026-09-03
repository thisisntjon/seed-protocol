STATE:       DONE
OBJECT:      Apply public-display SPEC Wave A (front door + hygiene); do not flip visibility. The SPEC and board tickets are banked in git history at commit b41ed67, not in the tree
EXACT_REF:   working-tree-2026-09-01-public-display-wave-a
EVIDENCE:    `python scripts/onboard_check.py` 0 errors; `python scripts/sabotage_test.py` 18/18; `python scripts/poc_check.py` 22/22; `python workflow/blueprint/bin/selftest.py` PASSED; `python workflow/harvest/pack/assemble.py --check` PASSED; `python workflow/blueprint/bin/orient.py` prints THE WHOLE JOB; `python workflow/research/2026-08-24-pr-case-study/measure_pr_census.py` exits 2 without a clone path; `JUDGES.md` exists; README has no `(private)` token
PROGRESS:    INFRASTRUCTURE
EFFECT:      none — infrastructure
BLOCKED_ON:  none
SESSION_ID:  12adcdea-fa5b-4bbe-b120-b1d0aa4f90cf
NEXT_OWNER:  later board — H2 dest-poison in selftest; human — GATES publication if flipping visibility
