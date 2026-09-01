# Harvest inventory — what can be repurposed

**Stamped:** 2026-08-23
**Machine file:** `INVENTORY.json` (schema `bonkers.harvest_inventory/v2`)
**Package:** `pack/`
**Check:** `python workflow/harvest/pack/assemble.py --check`
**Rows:** 93 — 10 CORE, 12 OPTIONAL, 8 IDENTITY, 45 CANDIDATE, 18 NEVER

This is the classified list of reusable **files** versus campaign mill. The harvest's
actual asset is the **ideas ledger**: `IDEAS.md` (145 development ideas). Files below
are how some of those ideas are already encoded. It is **not** a merge of Pokemon,
Career, Bonkers, and thebus.

## Classes

| Class | Meaning | Install |
|---|---|---|
| **CORE** | Default `transplant.py` allowlist. Already in this repo. | `python scripts/transplant.py --target <git> --apply` |
| **OPTIONAL** | In this repo; copy only with a named extra. | `assemble.py --dest <git> --extra comms,ops,poc,ci,canon` |
| **IDENTITY** | Shape yes, live contents never copy. | Greenfield: `assemble.py` writes **empty templates**. Existing project: keep theirs. |
| **CANDIDATE** | Exists in Pokemon/playbook/skills; extract or reimplement. | Named incident, then rebuild. Do not dump. |
| **NEVER** | Campaign, secrets, product UI, retired bus, domain mill. | Cannot enter a factory install. |

## Decision this inventory informs

Do **not** merge Pokemon + Career + Bonkers into one mega-repo. Transplant CORE. Load OPTIONAL
by extra. Keep domain packs in their origin repos.

Two install paths:

1. **Existing project** that already has a START-HERE of its own → `transplant.py` (CORE only).
2. **Greenfield git repo** → `assemble.py` (CORE + identity templates + optional extras).

`scripts/transplant.py` `PORTABLE_FILES` is not expanded by this harvest.

## CORE (the factory)

Already copied by transplant. Enough to not start over:

`LAWS.md` · `onboard_check.py` · `sabotage_test.py` · `status.py` · `checkpoint.py` ·
`transplant.py` · DISPATCH · RECEIPT · HANDOFF · EXPERIMENT templates.

## OPTIONAL (in this repo, not default)

| Extra | What | When |
|---|---|---|
| `comms` | `relay.py`, selftest, `workflow/relay/` README + profiles | Two harnesses on one repo. **Skip** `relay/beliefs/`. |
| `ops` | `spend_check.py`, `stress_test.py` | Unattended spend or scale sabotage |
| `poc` | `poc_check.py`, `poc_status.py`, `pocs/` fixtures | 15-minute cold-start scorer + deceptive-green. Rewrite evidence paths. |
| `canon` | Empty RETRACTIONS / DECISIONS / CLAIMS / GATES templates | Target fills values |
| `ci` | `.github/workflows/verify.yml` | GitHub Actions |
| `pack` | `assemble.py` itself | So a child project can re-export |

Default transplant **does not** grow these until each extra has a sabotage fixture (Law 2).
That is Phase 2 of this harvest, not this pack.

## IDENTITY (shape only)

START-HERE, AGENTS, CLAIMS, GATES, PLAN, README, live DECISIONS/RETRACTIONS, this repo's
blueprint architecture. `pack/identity/` holds empty templates for greenfield.

## CANDIDATE (rebuild, do not dump)

Portable **patterns**. Full rows in `INVENTORY.json`. Condensed here.

**From playbook (encode, don't paste 73 mixed rows):**

- UNIV rules → `pack/candidate/UNIV-RULES.md`
- Tool tiers 1–4 → `pack/candidate/TOOL-REBUILD.md`
- METRICS / COST / BOOTSTRAP as *patterns*
- Fleet templates (KANBAN, INBOX, GRAPH, ORCHESTRATOR, ROSTER, AUTONOMY, DEADLINES) when a
  second agent joins

**Rebuild when the trigger fires:**

| Trigger | Rebuild |
|---|---|
| Day 0 | CORE (already). Then `orient.py` as one command. |
| Second harness | `new_harness.py` shape, `verdict_lint.py`, dispatch ledger, stall watch, inbox-wake **policy** |
| Board file exists | Pokemon `status.py` ownership linter (different object from Bonkers `status.py`) |
| Unattended jobs | `gate_pin.py`, `queue_worker.py`, `ops_digest.py`, VALUE-delta heartbeats |
| Two boxes | `wt_sweep.py`, recovery runbook, dual-channel watchdog |
| Shipping to a runtime | `preflight.py` **rebuilt for that runtime**, SHA identity before spend |
| One north-star science graph | answer-map method (GSN/AIEG) as docs, not YAML from PTCG |

**Skills (live in `~/.claude/skills`, not this pack):** `phased`, `board-*`, `qol-baseline`,
`handoff`, `daemon`, `progress`, `align`, `end-session-closeout`, `spec` / `spec-critic` / `tdd`.
Copy a skill into a project only if that harness cannot see user skills.

## NEVER

Humanizer, `web/`, `relay/beliefs/`, this repo's receipts/experiments/measurements/handoff
instances, `SLOP_RETRACTIONS.md`, ~326 `ptcg-agent/harness` domain scripts, engine/card/kaggle/
episodes, research novels, Write-Up, Career pipeline, **thebus**, Pokemon campaign `AGENTS.md` /
`START-HERE.md`, seat inboxes, ship kernels, Godot/Comfy/UI-QA/Miracle/peek/grail skills,
box-specific `.ps1`/`.vbs` wake drivers.

## How to use the pack

```text
python workflow/harvest/pack/assemble.py --check
python workflow/harvest/pack/assemble.py --dest /path/to/new.git
python scripts/transplant.py --target /path/to/existing.git --apply
```

See `pack/README.md`.
