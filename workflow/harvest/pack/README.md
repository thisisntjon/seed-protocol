# SEED factory pack

Clean extract of Bonkers protocol. **Not** the Pokemon campaign. **Not** Career. **Not** thebus.

Two install paths. Do not mix them up.

## Existing project (already has identity files)

```bash
python scripts/transplant.py --target /path/to/existing.git --apply
```

Writes only CORE. Refuses if the destination already differs. Records hashes in
`workflow/SEED-TRANSPLANT.json`. Does **not** overwrite START-HERE / AGENTS / PLAN / GATES /
CLAIMS — those are the target's identity.

Dry run (no `--apply`) prints the plan.

## Greenfield (empty git repo)

```bash
git init /path/to/new-project
python workflow/harvest/pack/assemble.py --dest /path/to/new-project
```

Copies CORE from this repo, plus **empty** identity templates (START-HERE, AGENTS, GATES,
CLAIMS, PLAN, DECISIONS, RETRACTIONS). Then fill the four-line job in START-HERE and the
problem in PLAN. Run `python scripts/onboard_check.py` in the target.

Optional extras:

```bash
python workflow/harvest/pack/assemble.py --dest /path/to/new-project --extra comms,ops,poc,ci
```

`--extra canon` is already implied by greenfield identity templates.

## What CORE is

| Layer | Files |
|---|---|
| Laws | `LAWS.md` |
| Checks | `onboard_check.py`, `sabotage_test.py`, `status.py`, `checkpoint.py` |
| Comms schemas | DISPATCH, RECEIPT, HANDOFF, EXPERIMENT |
| Self-install | `transplant.py` |

That is the clone-and-go protocol. It is enough to not start over.

## Optional extras (not default)

See `MANIFEST.json` `optional`:

- **comms** — two harnesses, digest orbit, repo wins on facts. Does not copy `relay/beliefs/`.
- **ops** — spend window + randomized sabotage.
- **poc** — 15-minute cold-start scorer + deceptive-green. Rewrite evidence paths after copy.
- **ci** — GitHub verify workflow.
- **canon** — empty ledgers (greenfield already has these).
- **pack** — this assembler, so a child can re-export.

Do not copy `humanizer_*` or `web/`.

Law 2: extras stay out of default `transplant.py` `PORTABLE_FILES` until each extra has a
sabotage fixture. That is harvest Phase 2.

## Candidate docs (not installed unless you ask)

- `../IDEAS.md` — **the factory.** 145 development ideas used during the origin campaign.
  This is the asset. CORE files encode a subset.
- `candidate/UNIV-RULES.md` — UNIV rows extracted from the playbook ledger. Encode; do not
  paste FLEET/PROJ.
- `candidate/TOOL-REBUILD.md` — when to rebuild which tool. Not a dump of ~326 harness scripts.

Pass `--candidate` to copy those files into `workflow/factory/` of the destination.

## Validate this pack

```bash
python workflow/harvest/pack/assemble.py --check
```

Fails if a MANIFEST path is missing, if CORE drifts from `transplant.py`, or if a NEVER
path appears in CORE/OPTIONAL.

`scripts/sabotage_test.py` is the **source-repo** guard. Run it here, not on a dest that
has not been committed: `transplant.py` refuses to act as a source without a git HEAD.

## What this pack is not

- A merge of every Pokemon harness script
- An answer-map of PTCG science
- thebus (retired)
- A second protocol alongside the blueprint — it **feeds** `workflow/blueprint/ARCHITECTURE.md`

Inventory and class decisions: `../INVENTORY.md`.
