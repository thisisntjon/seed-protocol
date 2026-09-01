# Tool rebuild order — patterns, not a mill import

Source: `poketcg/playbook/TOOLS.md`. Instance paths there are under `scripts/` and
`ptcg-agent/harness/`. On a new project both layers can live in one `ops/` directory.

**Do not copy ~326 harness scripts.** Rebuild the abstract tool when its trigger fires.
Each rebuild is stdlib-only, fail-closed, exit-code API, and cites its incident in-source.

Bonkers CORE already covers day-0 protocol checks. This file is the rest.

## Tier 1 — day 0 (you cannot run a board without these)

| Tool | What it does | Already in CORE? | Rebuild when |
|---|---|---|---|
| docs-vs-reality checker | claimed paths exist; schemas hold | yes (`onboard_check.py`) | — |
| sabotage suite | guard fails on seeded defects | yes (`sabotage_test.py`) | each new guard |
| progress from PLAN | no second state file | yes (`status.py`) | — |
| checkpoint gate | refuse git checkpoint while red | yes (`checkpoint.py`) | — |
| transplant | non-destructive CORE install | yes (`transplant.py`) | — |
| board linter (`status.py` in Pokemon) | card ownership vs git | **no** — different object | a kanban/board file exists |
| worktree bootstrap | one handle, one persistent worktree | no | a second harness shares the repo |
| `orient` | SHA + PLAN stage + gates + newest handoff; refuse remembered state | no | first cold session after day 0 |

## Tier 2 — when the second agent joins

| Tool | What it does |
|---|---|
| `verdict_lint` | exactly one controlled verdict token per evidence PR |
| `dispatch_ledger` | every order gets a row; `list --unconfirmed` recovers crash-lost dispatches |
| `stall_watch` | MISSING/STALE heartbeats; overdue verifications |
| inbox wake **policy** | own-inbox SHA diff + <=30 min time baseline. Adapt per harness. Do not copy `.ps1`/`.vbs` drivers |
| waitgraph + prose-wait detectors | waits are `blocked_on` fields |
| `fleet_view` | one-screen roster + heartbeats |
| `wt_sweep` | repair-before-prune; dry-run default; KEEP ambiguous |

Lead monitor / movement audit: only if a lead is routing multiple workers.

## Tier 3 — when jobs outlive sessions

| Tool | What it does |
|---|---|
| `gate_pin` | gate frozen = pre-result blob+commit on the shared remote |
| `clearance` | <60s STOP checks; checklist is project-specific |
| `queue_worker` | OS-scheduled courier; fail-closed; caps; PARK on failure |
| `ops_digest` | daily digest; every section exception-swallowed |
| heartbeat + atomic checkpoint | VALUE-delta, not ACTIVITY-delta |
| recovery runbook | per box; watchers live **outside** worktrees |

## Tier 4 — when results start shipping

| Tool | What it does | Warning |
|---|---|---|
| `preflight` | simulate the **exact** production loader on the **exact** bytes | rebuild per runtime; do not copy the Kaggle bundle preflight |
| identity / submit check | SHA vs refs ledger before spend | — |
| `bank_lint` / `state_check` | prose-vs-table drift; handoff SLA | — |
| `eresolve` | sequential experiment IDs; fail closed on duplicates | — |
| `board_sync --check` | board vs git/PR. Never bulk `--apply` on a header-driven board | — |

## Pattern behind all of them

1. stdlib-only, read-only where possible
2. exit codes are the API
3. fail closed, loudly — cannot measure ⇒ failure, never silence
4. each check cites its incident in-source

## Never rebuild-by-copying

Eval, selfplay, search, deck, replay, ladder, oracle, loss, label, dagger, value, kernel
extractors, episode parsers, box-specific watchdogs, public kernel copies, engine bindings.
Those are the campaign mill (`INVENTORY.json` NEVER class).
