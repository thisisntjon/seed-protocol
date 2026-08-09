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
NEXT_OWNER:  <who/what consumes this: a seat, the lead, a gate, "none — terminal">
```
