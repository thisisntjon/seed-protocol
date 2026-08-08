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
         synthesis gate before roadmap. Triage depth to stakes — not everything is Deep.
CLAIM    state what you are taking and its acceptance criteria BEFORE building
         (fleet mode: claim-by-pushed-branch; solo mode: a dispatch note to yourself).
BUILD    smallest verifiable increment. Acceptance criteria are locked before the builder
         starts and are not edited by the builder. Two failed attempts = stop, write it up.
VERIFY   run the pre-registered check against the deployed-form artifact (Law 3). Positive
         results get independent reproduction (Law 4).
BANK     write a receipt (workflow/templates/RECEIPT.md) into workflow/receipts/. Update
         RETRACTIONS.md if anything previously banked is now false.
HANDOFF  before ending: update or write workflow/handoffs/<date>.md so a cold session
         resumes in ≤15 minutes. Shorter than the last one is the goal.
```

## Communication protocol

- **Everything travels through git artifacts.** No claim exists until it is in a file; no file is
  authoritative if `onboard_check.py` is red.
- **Dispatches** (work handed to an agent) follow `workflow/templates/DISPATCH.md` — object,
  exact ref, acceptance, fences, next event. A dispatch without acceptance criteria is invalid.
- **Receipts** follow `workflow/templates/RECEIPT.md` — state, evidence, blocked-on, next owner.
  "Done" without evidence is not a state.
- **Numbers**: check `workflow/canon/RETRACTIONS.md` before citing; cite with provenance
  (file + date) or not at all.
- **Decisions**: check `workflow/canon/DECISIONS.md` before proposing; settled questions are not
  re-opened without new evidence, and new decisions are recorded there same-session.
- **Escalation to the human**: aggregate everything human-bound into one block; only items on the
  `GATES.md` list qualify. While a pre-authorized runway exists, "awaiting adjudication" is not a
  legal idle state — do the next authorized thing.

## Fleet mode (opt-in, not default)

Scale to parallel workers ONLY when tickets are independent and worktree-isolatable (Law 8).
Then: main is lead-write-only (structural message authenticity), workers claim by pushing a
branch (branch existence = the lock), heartbeats must carry work counters (a PID alive is not
health), and every seat runs this same contract.
