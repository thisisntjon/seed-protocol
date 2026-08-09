HYPOTHESIS:      On matched project tasks, SEED reduces invalid completion claims without materially reducing correct task completion or increasing live human intervention.
OBJECT:          Treatment protocol begins from SEED portable identity `e46361ecc2a96355c3a064735e5ca501c2a38cb12e701cc35f41107c9d7f965b`; task corpus, model identity, and arm artifacts must be hashed before execution.
DEPLOYED_FORM:   Twelve randomized matched task pairs in isolated fresh repositories: bare project instructions versus the same project plus SEED, using the same model version, context/token ceiling, tools, time limit, and acceptance tests.
MEASUREMENT:     Primary endpoint is invalid completion claims per arm under blinded acceptance tests, including seeded evaluator, stale-state, and evidence-identity defects. Secondary endpoints are correct task completion, recovery time, live human intervention minutes, tokens, and verified decision/measurement loops. Pairing and stopping rule are fixed before the first run.
PASS_BAR:        SEED reduces invalid completion claims by at least 25 percentage points with a paired 90% interval excluding zero, while correct completion is not lower by more than 5 percentage points and median live-human minutes are not more than 20% higher.
KILL_BAR:        SEED produces no reduction in invalid completion claims, reduces correct completion by more than 10 percentage points, or increases median live-human minutes by more than 50% without a correctness gain.
COST:            Not authorized for execution yet; price the fixed twelve-pair run before opening a spend or compute gate.
OUTCOME:         PENDING
INDEPENDENT_REPRO: Required for any PASS; analysis must be performed from blinded arm labels.
