# Worker protocol (read this before touching a ticket)

You are one of several independent agents — possibly running in **different CLIs
and different harnesses** — draining a shared ticket board. Coordination is via
git and `board/board.py` only; there is no live channel between workers. Follow
this protocol exactly so we never collide, double-claim, or leave the tree dirty.

## The one-ticket loop

Repeat until `board.py next` prints `none`:

1. **Sync.** `git fetch && git pull --rebase` (skip if there is no remote).
2. **Select.** `python board/board.py next --harness <you>` → a ticket id (or
   `none`, meaning stop). Selection already skips tickets whose dependencies
   aren't `done` and respects priority.
3. **Claim (atomic).** `python board/board.py claim <ID> --owner <your-id>`.
   - Success → you own it. Proceed.
   - `conflict:` → another worker got it. Go back to step 2.
   - If there's a git remote, also `git push` the claim commit immediately; if
     the push is rejected, someone claimed first — run `set-status <ID> todo`
     to release and pick another.
4. **Isolate.** Create the worktree and branch named in the ticket:
   ```
   git worktree add <worktree_root>/<ID> -b ticket/<ID>
   cd <worktree_root>/<ID>
   ```
   Never do ticket work in the main checkout — that's how parallel workers
   clobber each other.
5. **Work.** Read the ticket's Goal / Context / Acceptance criteria. Do exactly
   that ticket — resist scope creep; new work becomes a new ticket, not a bigger
   PR. Commit in small steps.
6. **Heartbeat.** At least every ~15 minutes of active work, run
   `python board/board.py heartbeat <ID> --owner <your-id>` (from the main
   checkout or with `--` cwd set to the repo). This is how board-watch knows
   you're alive and not wedged.
7. **Verify.** Run every command in Acceptance criteria. All must pass. If you
   can't make them pass, go to Blocked (below) — do not open a green-looking PR
   over red tests.
8. **Ship.** Push the branch and open the PR:
   - `pr_mode: gh` → `git push -u origin ticket/<ID>` then
     `gh pr create --fill --base main --head ticket/<ID>`.
   - `pr_mode: record` (no GitHub) → write `board/prs/<ID>.md` with the branch
     name, a summary, and the diff stat; commit it.
   - Then: `python board/board.py set-status <ID> in_review --pr <url-or-path>`.
9. **Release & repeat.** The worktree can stay (the reviewer may want it) or be
   removed with `git worktree remove <worktree_root>/<ID>` once merged. Return
   to step 1.

## Blocked / failure

If a ticket can't proceed (dependency actually incomplete, ambiguous spec,
failing environment, needs a human decision):
```
python board/board.py set-status <ID> blocked --note "why, in one line"
```
This releases the claim lock so it's visible to the watcher and re-dispatchable.
Then pick the next ticket — don't spin on a blocked one.

## Rules

- **One ticket at a time per worker.** Finish or block before claiming another.
- **Stay in your worktree.** No edits in the main checkout, no touching another
  ticket's branch.
- **The board is the source of truth**, not your memory. Re-read `next`/`show`
  after any interruption.
- **Don't hand-edit `BOARD.md` or another worker's ticket status.** Only change
  status via `board.py`, and only for the ticket you own.
- **Leave the tree clean.** Every logical step is a commit; no stray files.
