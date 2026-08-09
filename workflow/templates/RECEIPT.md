# RECEIPT — work reported done

Bank one file per completed dispatch into `workflow/receipts/`, named
`<date>-<short-slug>.md`. The linter requires the STATE, EVIDENCE, and NEXT_OWNER fields.
"Done" without evidence is not a state (Law 5).

```
STATE:       DONE | PARTIAL | BLOCKED | KILLED | INVALIDATED
OBJECT:      <what this receipt is about>
EXACT_REF:   <commit/artifact hash the evidence was produced against>
EVIDENCE:    <command output, file path, hash, or measurement that proves the state —
              something a verifier can re-run or re-read>
PROGRESS:    DECISION | MEASUREMENT | INFRASTRUCTURE
EFFECT:      <the decision changed or measured outcome; use "none — infrastructure" honestly>
BLOCKED_ON:  <only if BLOCKED: the precise missing thing and who owns it>
SESSION_ID:  <the session/transcript identifier that produced this work — required for receipts
              dated 2026-08-09 or later; makes every verdict pairable to its trajectory>
ACTUAL:      <optional but expected when the dispatch carried a FORECAST: actual duration /
              tokens / attempts — the flywheel grades forecast vs actual>
NEXT_OWNER:  <who/what consumes this: a seat, the lead, a gate, "none — terminal">
```
