# DISPATCH — work handed to an agent

Copy, fill every field, deliver as a file (fleet: the worker's inbox; solo: alongside the plan).
A dispatch missing ACCEPTANCE or FENCES is invalid — the linter treats it as malformed.

```
TO:          <seat/session that owns this>
OBJECT:      <the one thing being worked on — file, feature, question>
EXACT_REF:   <commit hash / artifact hash / version this work is against>
ACTION:      <what to do, in one sentence>
ACCEPTANCE:  <the command(s) or observable(s) that define done — runnable, not vibes>
FENCES:      <what is out of bounds: files not to touch, decisions not to make, spend limits>
NEXT_EVENT:  <what happens when done: who consumes the receipt, what it unblocks>
```
