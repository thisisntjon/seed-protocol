# UNIV rules — extract, do not dump the mixed ledger

Source: `poketcg/playbook/RULES-LEDGER.md` (port column = UNIV only).
This file is a **candidate**. Encode what this project actually hits. Do not paste FLEET or
PROJ rows. Do not paste the origin campaign's numbers.

The playbook header claim that "every encoded rule never failed again" is **unverified**
(`workflow/canon/DECISIONS.md` caveat, 2026-08-18). Encoding is still the cheap default.
Measure recurrence on this project; do not treat the header as evidence.

## Solo default (encode these first)

| Rule | Encode as |
|---|---|
| State lives in files a cold session can read; never act on remembered state | `orient` + START-HERE + PLAN stage line |
| Producer owns the bridge: DONE = consumer's exact filename, sha-verified, on the watched surface | receipt schema + path check |
| Identity by hash, never label | transplant provenance; any ship preflight |
| Frozen criteria are immutable post-result; one failed criterion = bank the negative | EXPERIMENT.md outcomes; no free-text verdict |
| Exactly one machine-readable verdict token | `verdict_lint` when PRs are the evidence surface |
| Author XOR verifier for positives | AGENTS.md; do not self-grade |
| New instruments pass a one-time sabotage check before verdicts count | `sabotage_test.py` (already CORE) |
| Irreversibles are human-only and gates carry an SLA | `GATES.md` + onboard_check |
| Retracted tokens must not be re-cited outside the ledger | RETRACTIONS.md + onboard_check |
| Incidents add a check, never a new prose paragraph | LAWS.md meta-law |
| Claim-by-push; branch existence is the lock | when more than one writer exists |
| Every commit carries a handle as git author | when more than one writer exists |
| Waits are fields (`blocked_on`), not prose | when a second agent can block |
| Heartbeats carry VALUE-delta, not ACTIVITY-delta; silence is an event | when jobs outlive the session |
| Unattended writers carry byte + wall + disk caps and a runner-owned verdict | when unattended compute starts |
| Queue admission is fail-closed; failure PARKS | `queue_worker` when a courier exists |
| Bulk data requires a named consumer in flight | standing fence |
| Rigor at promotion boundaries; construction runs free | doctrine |
| Error budgets loosen when healthy | doctrine |
| Transcribe, don't paraphrase, when folding findings into pre-regs | dispatch discipline |
| Pre-register families/sweeps, not single configs, when iteration is expected | EXPERIMENT.md |

## When a second agent joins (still UNIV, not yet CORE)

Inbox is lead-write-only. Wake on your own inbox SHA diff. Dual-trigger: event watcher +
time baseline. Stale-order: consume the entire backlog; later entries supersede. Questions to
the lead go via `state=BLOCKED`. The human is never the courier. Protocol changes broadcast to
all inboxes. Prefer standing orders over per-instance routing. Verifier that FAILs holds a
standing re-verify on the next SHA. PR class tokens + self-engage. Escalation tiers so the
human is not paged for SEV2.

## FLEET (not in this extract)

Two boxes, hub checkout ban, worktree repair-before-prune, broker-is-not-delivery, dual-channel
box liveness, recovery runbook with watchers **outside** git worktrees. Rebuild when a second
machine exists. See `TOOL-REBUILD.md`.

## PROJ (do not copy)

Kaggle submission merit gates, organizer-material compliance, local-eval-as-filter-until-ladder,
board_sync apply ban, squad-prompt-in-message hook. Shape may be universal; parameters are not.

## How to use

1. When an incident happens here, add a **check** (Law 1) and a **LAWS.md** row if it is load-bearing.
2. Do not grow CORE by copying this table into `LAWS.md`.
3. A row here that this project has never hit stays a candidate.
