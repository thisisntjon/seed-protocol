# Blueprint — factory for building other systems

Miracle is an evolving media suite: capabilities compose under governance, each with an
inspectable deliverable. **This blueprint is the same idea for development systems.**

It is how tens of thousands of dollars of compute and thousands of human hours spent on
the origin campaign get reused, instead of being rebuilt per project.

```
clone or bootstrap → orient → work → checkpoint → (limit) → switch → orient → resume
```

Solo default. Fleet is an opt-in module. Pokémon, Career, and Miracle media stay in their
repos. This factory does not merge them.

## Start here

| You want | Open |
|---|---|
| What this is, in one screen | this file |
| Architecture (six layers + Miracle compose model) | `ARCHITECTURE.md` |
| What capabilities exist and their proof | `CAPABILITY-CATALOG.md` |
| Where each idea was taken from | `EXTRACT-LOG.md` |
| Living build plan | `PLAN.md` |
| Doctrine index (145 ideas) | `../harvest/IDEAS.md` |
| Install into a new git repo | `python bin/bootstrap.py --dest <repo>` |
| Cold start any session | `python bin/orient.py` |
| Prove the factory is not decorative | `python bin/selftest.py` |

Existing SEED tools still run at repo root: `scripts/onboard_check.py`,
`scripts/sabotage_test.py`, `scripts/transplant.py`.

## The compose model (from Miracle, adapted)

| Miracle | Here |
|---|---|
| Request | Problem statement (`/phased`) |
| Plan | `workflow/PLAN.md` (project) + this `PLAN.md` (factory) |
| Graph | Phases with dependencies; freeze bars before runs |
| Run | A phase execution that leaves receipts |
| Artifact | Receipt / experiment / code hash — identity by hash |
| Review | `GATES.md` human checkpoints with SLA |

A capability is not “the code exists.” It answers five questions (Miracle deliverable
standard): user job, proof artifact, location, quality checks, remaining work.

## What you get on day 0 (solo)

CORE protocol (laws, checkers, sabotage, dispatch/receipt/handoff/experiment, transplant)
plus orientation (`bin/orient.py`) plus this catalog. That is enough to not start over.

Load fleet templates under `templates/fleet/` when a second agent joins — not before.

## Invariant

A rule is not in the factory until it has an executable check **or** is marked PROSE
candidate. ENCODED without a sabotage fixture is a bug (`bin/selftest.py` fails it).
