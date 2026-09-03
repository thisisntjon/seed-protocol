# Extract log — file by file

**Stamped:** 2026-08-23
**Purpose:** Prove the blueprint was harvested from named sources, not invented. Each row is
a source file, what was taken, and where it landed. Domain mill (Pokémon engine, decks,
ladder µ, Kaggle kernels) is **not** taken.

Tuition this extract is meant to stop re-paying: tens of thousands of dollars of compute
plus thousands of human hours. The mill is the waste product. These files are the yield.

## Miracle (pattern for an evolving suite)

| Source | Taken | Landed | Left behind |
|---|---|---|---|
| `miracle/README.md` | Start-here split: working-in-repo vs running-the-app vs current-state | `blueprint/README.md` | videowatcher, media paths |
| `miracle/docs/suite-workflow-architecture.md` | Request → Plan → Graph → Run → Artifact → Review. Tool contract: id, inputs, outputs, approval, cost, risk. Miracle is control plane, not a tool playground | `capabilities/00-compose/` | MCP/provider graph DB |
| `miracle/deliverables/README.md` | Five questions every capability must answer; deliverable ≠ code-exists | CAPABILITY-CATALOG.md + every capability README | media sample packets |
| `miracle/deliverables/feature-deliverable-template.md` | User job / deliverable / location / quality bar / remaining work | `templates/CAPABILITY.md` | — |
| `miracle/deliverables/feature-inventory.md` | Completed / partial / not-started with proof column | CAPABILITY-CATALOG.md | C1–C34 media features |
| `miracle/docs/swiss-army-knife-status.md` | Local-first; crude-but-real; composition is the product; harden before adding surface | ARCHITECTURE.md v1 posture | promo_video.v1 |
| `miracle/master-skills-catalog.md` | Portable vs path-bound skills; copy SKILL.md not machine paths | `capabilities/09-method/` + `06-adapters/` | Group B portfolio skills |
| `miracle/workflow/PLAN.md` + `LEDGER.md` | Living plan + ownership ledger as the suite's memory | `blueprint/PLAN.md` | Miracle phase numbers |
| `miracle/deliverables/workflow-ledger/` | Runs leave inspectable artifacts | receipts + LEDGER.jsonl idea | SQLite schema |
| `miracle/deliverables/approval-gates/` | Paid/external steps require persisted approval | GATES.md + Law 7 | provider spend UX |
| `miracle/deliverables/hardening-baseline/` | Queue/recovery/idempotency before new features | `capabilities/05-operations/` | worker leases |
| `miracle/docs/everything-suite-mcp-roadmap.md` | Suite grows by adding governed capabilities, not by merging repos | DECISIONS 2026-08-23 | MCP tool list |

## Pokémon playbook (portable operating model)

| Source | Taken | Landed | Left behind |
|---|---|---|---|
| `playbook/README.md` | Eight load-bearing ideas + movement-wave ninth | `capabilities/00-compose/` thesis | Instance roster names |
| `playbook/PLAYBOOK.md` | Roles, claim-by-push, mailbox, dual-trigger, waits-as-fields, flywheels, staging ladder, error-catching layers, continuity, five transferable claims | families A–G in IDEAS.md; fleet templates | Worked-example PTCG flywheels |
| `playbook/BOOTSTRAP.md` | Three human answers first; day 0–3 sequence; copy vs re-derive; anti-patterns; MVS = solo+2 at ~1/5 tooling | `bin/bootstrap.py` docs; `capabilities/01-substrate/` | Instance branch names as required |
| `playbook/RULES-LEDGER.md` | UNIV rows only; ENCODED/CHANNEL/PROSE; named incidents | `rules/LEDGER.md` + pack/candidate/UNIV-RULES.md | FLEET/PROJ rows as default; unverified “never failed again” statistic |
| `playbook/TOOLS.md` | Tiers 1–4; fail-closed; exit-code API; incident-in-source; rebuild-when | `pack/candidate/TOOL-REBUILD.md`; `capabilities/05-operations/` | 326 harness scripts |
| `playbook/METRICS.md` | Four families: flow, liveness, quality, economy | `templates/METRICS.md` | Instance numeric baselines as targets |
| `playbook/COST.md` | Coordination waste > token waste; ZERO/LOW/NEEDS-GO levers; empty dollar table = principal-only | `capabilities/12-cost/` | Unfilled $/day cells; unverified Law-9 cash figure |
| `playbook/templates/AGENTS.md` | Worker contract shape | harvest identity AGENTS + CORE AGENTS | Fleet-only clauses as default |
| `playbook/templates/GATES.md` | Default NOT promotion-eligible; status vocabulary; append corrections | `templates/fleet/GATES-PROMOTION.md` | Empty of PTCG claims |
| `playbook/templates/AUTONOMY.md` | STOP tiny; LOG-AND-CONTINUE; error budgets loosen; two-strike parks lane | `templates/fleet/AUTONOMY.md` | Instance STOP rows 2+ |
| `playbook/templates/GRAPH.md` | Flywheels; producer owns the bridge; 15-min SLA | `templates/fleet/GRAPH.md` | Box names |
| `playbook/templates/PROTOCOL.md` | Mailbox + STATUS.json + wake/unblock/stale-order/cadence/daemon | `templates/fleet/PROTOCOL.md` | — |
| `playbook/templates/KANBAN.md` | Board as mutex + cycle header | `templates/fleet/KANBAN.md` | Cards |
| `playbook/templates/ROSTER.md` | Identity fixed, function fluid | `templates/fleet/ROSTER.md` | Names |
| `playbook/templates/ORCHESTRATOR.md` | Lead procedure | `templates/fleet/ORCHESTRATOR.md` | — |
| `playbook/templates/INBOX-example.md` | Entry format | `templates/fleet/INBOX-example.md` | — |
| `playbook/templates/DEADLINES.json` | Survives session death; re-arm from file | `templates/fleet/DEADLINES.json` | Dates |

## Pokémon method docs (discipline, not the game)

| Source | Taken | Landed | Left behind |
|---|---|---|---|
| `ptcg-agent/docs/EVAL_PROTOCOL.md` | Filter≠predictor; power rule; provenance stamp; configctl+verify+nonzero candidate counter; skipped checks ≠ pass; farm vs elite; latency mode | `capabilities/08-measurement/` | Ladder µ map, pin2, cg.dll ABI, opponent names |
| `workflow/DEAD-ENDS.md` | Scope guard on every negative; overstatement is the expensive failure; VOID vs UNKNOWN vs SOUND; arithmetic can close a door | `templates/DEAD-ENDS.md` | A1–A13 PTCG rows |
| `workflow/canon/DOC-ROLES.md` | Wake pack not 600 novels; inventories over memos; START-HERE wins vs AGENTS provenance | `capabilities/01-substrate/` | Path table of PTCG files |
| `workflow/canon/ARCHIVE-POLICY.md` | Never delete; archive banner + supersession | `templates/ARCHIVE-POLICY.md` | — |
| `workflow/canon/RETRACTIONS.md` (pattern) | Token ledger; mechanism not just the false number | CORE RETRACTIONS | PTCG tokens |
| `START-HERE.md` field facts | Which object/sha; reachable≠selected≠executed; freeze vs mature; pair-mean; point-bar false precision; unread path ≠ empty; derived ceiling ≠ wall | IDEAS C04–C08, D07 | Mission dates, c61, writeup slot |

## SEED (already executable)

| Source | Taken | Landed | Left behind |
|---|---|---|---|
| `LAWS.md` | Laws 1–9 + meta-law | CORE; `rules/LEDGER.md` maps to checks | Unverified $ figure as cash |
| `AGENTS.md` | Loop: orient-research-claim-build-verify-bank-handoff | CORE; `bin/orient.py` | — |
| `GATES.md` | Human-key + 48h SLA | CORE | Open/answered rows (identity) |
| `CLAIMS.md` | HYPOTHESIS default; SUPPORTED needs bound evidence | CORE identity template | Live C-001… rows |
| `scripts/onboard_check.py` | Docs vs reality | CORE | — |
| `scripts/sabotage_test.py` | Law 2 | CORE | — |
| `scripts/status.py` | Progress from PLAN table | CORE; orient consumes it | — |
| `scripts/checkpoint.py` | Refuse red checkpoints | CORE | — |
| `scripts/transplant.py` | Non-destructive CORE install | CORE | — |
| `scripts/relay.py` | Two-harness orbit | OPTIONAL comms | beliefs/ |
| `scripts/spend_check.py` | Law 9 | OPTIONAL ops | — |
| `scripts/stress_test.py` | Randomized sabotage | OPTIONAL ops | — |
| `workflow/templates/*` | DISPATCH/RECEIPT/HANDOFF/EXPERIMENT | CORE | — |
| `workflow/harvest/IDEAS.md` | 145 ideas, 10 families | This blueprint’s doctrine index | — |
| `workflow/harvest/pack/` | Greenfield assemble | `bin/bootstrap.py` wraps it | — |

## Skills (user-global; do not dump into CORE)

| Source | Taken | Landed | Left behind |
|---|---|---|---|
| `user-skills/`phased/` | Frame → investigate → roadmap → phase-loop; pivot-check | `capabilities/09-method/` | Skill runner paths |
| `user-skills/`qol-baseline/` | 22 operational features; scale to project; N/A is valid | `capabilities/05-operations/` | — |
| `user-skills/`board-lead|watch|work/` | Git-file board + worktree tickets | `capabilities/11-fleet/` deferred | board.py until 2nd agent |
| `user-skills/`handoff/` | Wrapup/pickup between PLAN and memory | CORE HANDOFF.md | hardcoded paths |
| `user-skills/`daemon/` | Registry of long-lived processes | `capabilities/05-operations/` | machine registry |
| `user-skills/`progress/` | Honest % from completed weights | optional | statusline wiring |
| `user-skills/`align/` | 3 steering questions when ambiguous | `capabilities/09-method/` | — |
| `user-skills/`spec` / `spec-critic` / `tdd` | Design/review/test loop | `capabilities/09-method/` | — |
| `user-skills/`end-session-closeout/` | Evidence-based close | HANDOFF + receipts | UI-QA stages |

## Explicitly not extracted

| Source | Why |
|---|---|
| `ptcg-agent/harness/*` (~326) | Domain mill (I-K01) |
| `ptcg-agent/agent/cg`, card PDFs, kaggle.json, episodes | Compliance + secrets |
| `ship_kernels/`, public_kernels | Competition payloads |
| `workflow/research/*` novels, ladder_log, writeup drafts | Campaign evidence |
| `Write-Up/` | Strategy-category product |
| Career pipeline JSON | Different product |
| thebus | RETIRED |
| SEED `humanizer_*`, `web/` | Product experiment, not protocol |
| Godot/Comfy/UI-QA/Miracle-MCP/peek/grail skills | Domain/product |
| Box-specific `.ps1`/`.vbs` wake drivers | Copy the policy (dual-trigger), not the files |

## How a future extract is added

1. Name the source file in this log.
2. Add or update an idea row in `workflow/harvest/IDEAS.md`.
3. If it ships as a check, add a `rules/LEDGER.md` row with a sabotage fixture.
4. If it is a capability, add a catalog row and a `capabilities/<id>/README.md` answering the five questions.
5. Do not copy the source tree.
