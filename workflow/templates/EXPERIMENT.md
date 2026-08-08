# EXPERIMENT — pre-registration

Commit this BEFORE results exist; the commit timestamp is the pre-registration (self-asserted
timestamps are unverifiable; pre-result commits are not). Outcomes are terminal — one of four
tokens, no free-text verdicts (Law 4).

```
HYPOTHESIS:      <one falsifiable sentence>
OBJECT:          <exact artifact under test — HASH, not label (Law 3)>
DEPLOYED_FORM:   <how the object is packaged/run for measurement — must match how it ships>
MEASUREMENT:     <the command/procedure; the sample size and why it is powered for the
                  effect size that would matter>
PASS_BAR:        <pre-stated threshold for shipping>
KILL_BAR:        <pre-stated threshold for abandoning — honored regardless of narrative>
COST:            <estimated spend/time; actual filled in at outcome — economics get measured>
OUTCOME:         PASS | KILL | NULL | INVALID-INSTRUMENT   (+ the measured value, + receipt path)
INDEPENDENT_REPRO: <required for PASS: who reproduced it, from what ref — author XOR verifier>
```
