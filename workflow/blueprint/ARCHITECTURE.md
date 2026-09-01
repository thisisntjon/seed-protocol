# Blueprint — draft architecture (v0)

A clone-and-go repository template for running agentic development projects that survive usage
limits, provider switches, and session death, without manual context management.

Status: **v0.1 building.** Written 2026-08-18; first executable extract 2026-08-23.
Catalog, file-by-file extract log, orient/bootstrap/selftest live under this directory.
Published view of the draft:
https://claude.ai/code/artifact/89126001-74c0-40a0-a00d-3ac69fe14a40

Relationship to this repo: **the blueprint supersedes SEED.** SEED is an input to it, not a peer.
See `workflow/canon/DECISIONS.md` (2026-08-18). Source material is `poketcg/playbook/` — 73 rules,
each recording the incident that produced it.

## What it has to solve

Three failures observed running poketcg. Every component below traces to one of them.

| Observed failure | Requirement | Layer that owns it |
|---|---|---|
| Hitting usage limits, switching providers mid-work | Any harness from any vendor can pick up the work without rebuilding shared understanding | 2 Orientation, 6 Adapters |
| Managing context manually — babysitting what each session knows | State lives on disk, bounded and current; no session is the sole holder of anything | 1 Substrate, 3 Continuity |
| No reuse — rebuilt per project | Day one of a new project is a clone plus one command | Whole template |

**Scope boundary.** Single strong agent is the default operating mode. Multi-agent scale-out is an
opt-in module, off in v1 — consistent with `DECISIONS.md` (2026-08-08) and with the playbook's own
minimum-viable-subset finding that a solo operator plus two agents yields the headline properties
"at roughly a fifth of the tooling."

## The six layers

Numbered by dependency: each layer assumes the ones above it. A layer can be adopted without the
ones below it.

### 1. Substrate — *ported*

The repo is the memory. One durable file per kind of fact: plan, gates, decisions, dispatch
ledger, receipts. Size-capped and **overwritten, never appended**, so a reader never wades through
archaeology to find current truth.

From the playbook's durable-state-files pattern and its handoffs-shrink-over-time health metric.
The failure it prevents: state living in a session's head and dying with it.

### 2. Orientation — *ported*

One command, `orient`, that any harness runs before acting. Reads the substrate, checks it against
git reality, prints current state and the next action. Bounded by an explicit budget so cold-boot
cost cannot creep.

Playbook target: successor productive in <= 15 minutes, re-reviewing nothing. Paired with the
stale-order rule — never act on remembered state.

### 3. Continuity — *new*

Checkpoint, hand off, switch, resume. State is written **continuously at milestones**, not at
wrap-up, because a usage cutoff gives no warning. Includes working-tree escrow so a half-finished
edit is recoverable, and a switch path that carries a project to a different vendor.

This is the layer poketcg lacked and the direct cause of the manual context management. Handoff
memo size is the health metric: it should shrink over time.

### 4. Enforcement — *new*

Rules are executable checks, not documents. Each check names the incident that earned it and
blocks on violation. Wired to pre-commit, CI, and harness hooks so the same rule fires regardless
of who is driving.

33 of the 73 playbook rules are already machine-enforced; 27 universal ones are still prose. This
layer is where the second group goes.

### 5. Operations — *ported*

Spend and usage visibility with a switch threshold; long-job heartbeats plus atomic checkpoints;
scheduled ticks driven by the OS scheduler rather than any session, so progress survives every
session dying at once.

Directly ported: the digest-from-scheduler pattern, the zombie-work rule (silence must never look
like health), and the watcher that over-fired and leaked spend.

### 6. Harness adapters — *new*

Per-vendor glue generated from one source: Claude Code hooks/skills/settings, Codex `AGENTS.md`,
Cursor rules. Conventions are written once; each adapter renders them into the form its harness
reads on boot.

Without this, cross-vendor switching means re-teaching conventions by hand — which relocates the
manual context management rather than removing it.

## End-to-end lifecycle

```
clone -> bootstrap -> orient -> work -> [checkpoint] -> [limit reached] -> [switch] -> orient -> resume
```

Bracketed steps do not exist today.

| Step | What runs | What it guarantees |
|---|---|---|
| bootstrap | `python bootstrap.py` | Substrate files created, checks installed to pre-commit and CI, adapters rendered for every harness present |
| orient | `python orient.py` | Current state verified against git, plus the single next action. Refuses to print stale state — flags drift instead |
| checkpoint | Milestone hook + pre-compaction trigger | Substrate is at most one milestone behind. Unplanned death costs one milestone, never a session |
| limit reached | Usage watcher at a configured threshold | Warning arrives before the wall, not at it. Triggers a checkpoint rather than a scramble |
| switch | `python switch.py --to codex` | Emits a paste-ready boot block for the target harness; escrows uncommitted work to a recoverable ref |
| resume | `orient` on the new harness | New session states its understanding back before acting; drift against the substrate is surfaced, not assumed away |

## Repository layout

```
workflow/blueprint/          (this directory — Miracle-style capability catalog)
  README.md                  factory front door
  ARCHITECTURE.md            this file
  CAPABILITY-CATALOG.md      SHIPS / PARTIAL / DOCUMENTED / DEFERRED
  EXTRACT-LOG.md             file-by-file provenance of the extract
  PLAN.md                    factory build plan (not SEED PLAN.md)
  bin/bootstrap.py           greenfield install (wraps harvest assemble)
  bin/orient.py              cold-boot; refuses missing START-HERE
  bin/selftest.py            catalog + ledger paths + orient sabotage
  capabilities/C00–C17       five-question READMEs (Miracle deliverable standard)
  rules/LEDGER.md            idea → check → sabotage
  templates/                 DEAD-ENDS, METRICS, EVAL-DISCIPLINE, ARCHIVE, fleet/

SEED CORE (already at repo root — not duplicated here)
  LAWS.md AGENTS.md GATES.md CLAIMS.md
  scripts/{onboard_check,sabotage_test,status,checkpoint,transplant}.py
  workflow/templates/{DISPATCH,RECEIPT,HANDOFF,EXPERIMENT}.md
```

Deferred vs the 2026-08-18 drawing: `switch.py`, `conventions.yml`+render, OS `tick.py`.
Those are PLAN B2. Do not pretend they ship.

## The enforcement invariant

One rule governs the whole template and is the reason it will not rot:

> **A rule is not in the blueprint until it has an executable check.**

`rules/LEDGER.md` carries an enforcement column, and `test_checks.py` verifies that column against
reality. Marking a rule ENCODED without a corresponding check that provably fails on a seeded
defect breaks the build.

| Class | Meaning | Treatment in v1 |
|---|---|---|
| ENCODED | A machine check blocks the violation | Ships. Must have a sabotage test |
| CHANNEL | The protocol makes violation structurally impossible | Ships. Preferred over ENCODED where available — a rule you cannot break beats one that catches you |
| PROSE | Written down only | Ships only as a documented candidate, never as a guarantee. Counted, and the count is visible |

Because every check records what it caught, the template accumulates per-rule violation data that
does not currently exist anywhere. That turns "encoded rules hold, prose rules do not" from an
untested claim into a measurement — see the caveat in `workflow/canon/DECISIONS.md`.

## In v1, and deferred

| Component | Status | Reasoning |
|---|---|---|
| Substrate, orientation, continuity | v1 | The three stated pains. Nothing else matters if these do not work |
| Rule checks (universal subset) | v1 | 60 of 73 rules are marked universal; they are the portable core |
| Spend visibility and switch threshold | v1 | Directly addresses hitting the wall without warning |
| Adapters: Claude Code, Codex | v1 | The two harnesses actually switched between |
| Multi-agent orchestration, mailbox, squads | deferred | Opt-in module. Canon closed the fleet default; the playbook's own MVS drops it too |
| Artifact broker, courier, cross-box watchdogs | deferred | Multi-box concerns. 7 of 73 rules; no current need |
| Project-specific rules | excluded | 6 of 73. Shape is universal, parameters are not — these become template stubs |

## Open questions

Decisions this draft does not make. Each changes the build materially.

1. **Naming and location.** What is the repo called, and does it live as its own public repo, a
   private one, or a directory inside an existing project? Affects whether adapters can be
   published for reuse and whether the rule ledger is citable.
2. **State format.** Markdown that a human reads and edits directly, or structured data with
   rendered views? Markdown is diffable and harness-agnostic but drifts from its schema.
   Structured data validates but needs tooling to read. The playbook used Markdown throughout,
   with mixed results.
3. **Switch trigger.** Does the usage watcher warn only, or actively halt work at the threshold?
   Warning preserves autonomy and can be ignored at exactly the wrong moment. Halting is safer and
   will sometimes stop useful work early.
4. **Triage sequence.** Triage all 73 rules before building, or build the three v1 layers first and
   triage against a working skeleton? Triage-first is the agreed plan and avoids baking in expired
   workarounds. Skeleton-first produces something usable sooner and gives the triage a concrete
   target to judge against.

## Provenance of the source material

`poketcg/playbook/RULES-LEDGER.md`, read 2026-08-18. Counted directly from the file:

- 73 rules, each with a named origin incident
- Portability: 60 UNIV, 7 FLEET, 6 PROJ
- Enforcement: 33 ENCODED, 8 CHANNEL, 31 PROSE (27 of the PROSE rules are UNIV)

**Caveat on the ledger's own headline finding.** Its header states "every encoded rule never failed
again, every prose rule was violated at least once." The ledger cannot substantiate this: its
columns are Rule / Origin incident / Enforcement / Port, where the origin incident is what
*created* the rule, not what happened after. There is no recurrence tracking in the file. An
external audit reports the claim originated as a 7-rule, 48-hour observation and was scaled to 73
rows. Treat it as an untested hypothesis. Encoding rules is still cheap and low-risk, and the
enforcement invariant above is what would finally measure it.
