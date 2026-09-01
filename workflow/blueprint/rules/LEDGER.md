# Rules ledger — factory enforcement

Maps portable ideas to checks that exist **in this repo**. ENCODED rows must name a path
that `bin/selftest.py` can see. PROSE is a candidate, not a guarantee.

The playbook headline “encoded never failed again” is **unverified** (DECISIONS 2026-08-18).
This table is how that claim becomes measurable.

| ID | Idea | Enforcement | Check | Sabotage |
|---|---|---|---|---|
| R01 | Docs match reality (I-A03) | ENCODED | `scripts/onboard_check.py` | sabotage: missing path |
| R02 | Retracted tokens stay in the ledger (I-A04) | ENCODED | onboard_check RETRACT | sabotage: nested citation |
| R03 | Gate SLA (I-E02) | ENCODED | onboard_check GATES | sabotage: overdue OPEN |
| R04 | Receipt has evidence (I-B09 spirit) | ENCODED | onboard_check ARTIFACTS | sabotage: receipt without evidence |
| R05 | Dispatch has ACCEPTANCE | ENCODED | onboard_check | sabotage: dispatch without acceptance |
| R06 | Experiment outcomes closed set (I-B02) | ENCODED | onboard_check | sabotage: invalid outcome |
| R07 | Handoff headings (I-A10) | ENCODED | onboard_check | sabotage: malformed handoff |
| R08 | SUPPORTED claim bound evidence (I-B04) | ENCODED | onboard_check CLAIMS | sabotage: supported without path |
| R09 | Sabotage before trust (I-B05) | ENCODED | `scripts/sabotage_test.py` | the suite itself |
| R10 | Progress ≠ throughput (I-H02) | ENCODED | `scripts/status.py` | sabotage: infra ≠ verified |
| R11 | Red checkpoint refused (I-G07 spirit) | ENCODED | `scripts/checkpoint.py` | (covered by status/onboard) |
| R12 | Identity files not overwritten (I-J07) | ENCODED | `scripts/transplant.py` | sabotage: refuse differing |
| R13 | Orient without START-HERE fails (I-G01) | ENCODED | `workflow/blueprint/bin/orient.py` | `bin/selftest.py` |
| R14 | Pack CORE matches transplant | ENCODED | `workflow/harvest/pack/assemble.py --check` | assemble --check |
| R15 | Incident → check (I-D03) | CHANNEL | meta-law in LAWS.md | — |
| R16 | Humans only irreversibles (I-E01) | CHANNEL | GATES.md list | — |
| R17 | Local eval ≠ predictor (I-C01) | PROSE | `templates/EVAL-DISCIPLINE.md` | encode per domain |
| R18 | Producer owns the bridge (I-F05) | PROSE | `templates/fleet/GRAPH.md` | encode at 2nd box |
| R19 | VALUE-delta not ACTIVITY (I-F12) | PROSE | PROTOCOL heartbeats | encode with first daemon |
| R20 | Scope guard on negatives (I-C17) | PROSE | `templates/DEAD-ENDS.md` | encode with first dead-end linter |
