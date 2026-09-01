# Capability catalog

Statuses: **SHIPS** (executable here) · **PARTIAL** (some proof, named gap) ·
**DOCUMENTED** (extracted; encode on next incident) · **DEFERRED** (opt-in fleet/box) ·
**EXCLUDED** (domain mill).

A row is not product-ready because code exists. Proof is the deliverable column.

| ID | Capability | Status | Proof | Target |
|---|---|---|---|---|
| C00 | Compose (request/plan/run/artifact/review) | DOCUMENTED | `capabilities/00-compose/README.md` | Projects start with `/phased` + receipts |
| C01 | Substrate (repo is memory) | SHIPS | onboard_check paths; START-HERE; templates | Wake pack stays small |
| C02 | Orientation | SHIPS | `bin/orient.py`; `bin/selftest.py` | ≤15 min successor |
| C03 | Continuity (checkpoint/handoff/switch) | PARTIAL | HANDOFF template + checkpoint.py; switch.py not built | `bin/switch.py` |
| C04 | Enforcement (rules as checks) | SHIPS | sabotage_test 18/18; rules/LEDGER.md | Recurrence measurement still open |
| C05 | Operations (spend, heartbeats, QoL) | PARTIAL | spend_check + stress_test optional; QoL checklist documented | OS digest / queue_worker on unattended |
| C06 | Harness adapters | DOCUMENTED | AGENTS.md paste-portable; harvest relay optional | conventions.yml + render.py |
| C07 | Evidence / promotion | SHIPS | EXPERIMENT.md + GATES SLA + CLAIMS | verdict_lint when PRs are the surface |
| C08 | Measurement discipline | DOCUMENTED | `capabilities/08-measurement/` from EVAL_PROTOCOL | Rebuild power/calibration per domain |
| C09 | Method (phased, existence-check, rule diet) | SHIPS | harvest PLAN + `/phased`; IDEAS D-family | — |
| C10 | Autonomy / human-key | SHIPS | GATES.md + Law 7 | AUTONOMY STOP table per project |
| C11 | Fleet | DEFERRED | `templates/fleet/` | Second agent incident |
| C12 | Cost / closed loops | PARTIAL | Law 9 + spend_check optional | Principal fills real $ |
| C13 | Dead-end register (scope guards) | DOCUMENTED | `templates/DEAD-ENDS.md` | First scientific negative |
| C14 | Metrics dashboard | DOCUMENTED | `templates/METRICS.md` | First unattended week |
| C15 | Archive / never-delete | DOCUMENTED | `templates/ARCHIVE-POLICY.md` | Research trees |
| C16 | Greenfield bootstrap | SHIPS | `bin/bootstrap.py` wraps harvest assemble | — |
| C17 | Non-destructive transplant | SHIPS | `scripts/transplant.py` | — |

Partial = some proof exists, named gap remains. That is Miracle's inventory honesty.
