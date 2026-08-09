HYPOTHESIS:      SEED's guards (onboard_check + spend_check) detect 100% of seeded defects
                 across all 16 injectable defect classes and raise zero false alarms on clean
                 copies carrying benign valid additions.
OBJECT:          scripts/onboard_check.py + scripts/spend_check.py at current working tree
                 (post-checkpoint 87171d5 lineage)
DEPLOYED_FORM:   invoked as subprocess against disposable repo copies, exactly as CI invokes them
MEASUREMENT:     scripts/stress_test.py --trials 250 --seed 20260809; ~70% defect trials
                 (random class, randomized parameters), ~30% clean trials with randomized
                 benign additions (valid receipts, gates, dispatches, experiments, handoffs);
                 spend_check scenarios generated with synthetic ccusage exports. Sample sizes
                 give ~10-12 trials per defect class.
PASS_BAR:        every defect class 100% detected AND 0 false alarms across all clean trials
KILL_BAR:        any defect class with a missed detection, or any false alarm -> hypothesis
                 KILLED; the gap is a real guard defect to fix, and green is not trusted until
                 a re-run passes
COST:            ~$0 API (pure local CPU); est. 10-20 min wall
OUTCOME:         PASS (2026-08-09: 250 trials, 17/17 classes at 100% detection across 145
                 defect injections; 0 false alarms in 80 benign trials; 25/25 spend_check
                 scenario verdicts correct; receipt 2026-08-09-guard-stress-250.md)
INDEPENDENT_REPRO: OWED - deterministic rerun is `python scripts/stress_test.py --trials 250
                 --seed 20260809`; a NON-AUTHOR session should rerun before this PASS is
                 treated as verified (this session authored both the guards and the harness,
                 so author-XOR-verifier is not yet satisfied). Scope caveat: measures
                 refutation power against the 17 modeled defect classes, not unknown-unknowns.
