# AGENTS — universal worker contract

Paste-portable: this file works verbatim in Claude Code, Codex, Devin, Cursor, or any harness
that can read files and run git. It is the contract; `LAWS.md` is the constitution.

## Roles and authority

| Role | Owns | Never does |
|---|---|---|
| **Human** | Irreversibles listed in `GATES.md`; answering gates within SLA | Courier work between agents; re-explaining state a file already holds |
| **Lead** (one session at a time) | The plan, routing, merges to main, the gate registry | Building and verifying the same object |
| **Worker** | Exactly the claimed ticket; its receipts | Self-merge, editing another agent's dispatch, acting past a fence |
| **Verifier** | Independent reproduction of positive claims | Verifying work it authored (author XOR verifier) |

Solo mode (default): one strong agent holds Lead+Worker; verification of positives still requires
a fresh session or different model — never the authoring context grading itself.

## The loop

```
ORIENT   read START-HERE → LAWS → GATES → workflow/PLAN.md → newest handoff. Files only.
RESEARCH if the plan's stage demands it: phased investigation, assumptions with kill criteria,
         synthesis gate before roadmap. Triage depth to stakes — not maximal.
CLAIM    state what you are taking and its acceptance criteria BEFORE building.
BUILD    smallest verifiable increment. Two failed attempts = stop, write it up.
VERIFY   run the pre-registered check against the deployed-form artifact (Law 3). Positive
         results get independent reproduction (Law 4).
BANK     write a receipt (workflow/templates/RECEIPT.md) into workflow/receipts/.
HANDOFF  before ending: update workflow/handoffs/<date>.md so a cold session resumes in <=15 minutes.
```

## Communication protocol

- **Everything travels through git artifacts.** No claim exists until it is in a file; no file is
  authoritative if `onboard_check.py` is red.
- **Dispatches** follow `workflow/templates/DISPATCH.md`. A dispatch without ACCEPTANCE is invalid.
- **Receipts** follow `workflow/templates/RECEIPT.md`. "Done" without evidence is not a state.
- **Numbers**: check `workflow/canon/RETRACTIONS.md` before citing; cite with provenance or not at all.
- **Decisions**: check `workflow/canon/DECISIONS.md` before proposing.
- **Escalation to the human**: only items on the `GATES.md` list. Aggregate into one block.

## Fleet mode (opt-in, not default)

Scale to parallel workers ONLY when tickets are independent and worktree-isolatable (Law 8).
Then: main is lead-write-only, workers claim by pushing a branch, heartbeats carry work counters.
