# Harvest — portable factory pack (living document)

Format: phased-investigation-workflow (`/phased`). Triage depth: **Light** — destination is
known (`transplant.py` + SEED laws); the failure mode is sprawl, prevented by a NEVER list.
Current stage: phase 4 — done (blueprint factory catalog + orient/bootstrap/selftest)
Last updated: 2026-08-23

> **Placement:** do **not** edit `workflow/PLAN.md` (SEED P1–P3, paused). Blueprint remains
> `workflow/blueprint/ARCHITECTURE.md`. This harvest feeds the blueprint; it does not replace it.

## Problem

**Problem:** Reusable *development ideas* earned in production (eval discipline, evidence
culture, session-death continuity, fleet ops, promotion gates) are trapped inside a Pokémon
campaign mill and a 10-file CORE pack. A file list is not the factory. The factory is a
growing ledger of ideas that other projects can encode as they hit the same incidents.

**Why now:** The principal asked for an inventory of everything that can be repurposed. The first
pass inventoried files to copy. The correction: inventory the ideas used *during* the
project — thousands of human hours of research — so SEED becomes an evolving factory.

**Original hypothesis:** (principal, 2026-08-23)

> Please create an inventory of everything that can be repurposed and create a clean
> package for it in the bonkers project.

**Corrected hypothesis:** (principal, 2026-08-23)

> Take all of the valuable development ideas that were used DURING the project and create
> that inventory for bonkers. The idea is to have a growing evolving factory that can be
> used for other items.

## Goal

A growing **ideas ledger** (`IDEAS.md` / `IDEAS.json`) of portable development doctrine,
plus a small **file pack** that already encodes a subset (CORE). New incidents add idea
rows, then checks. The mill does not enter this repo. Greenfield still uses `assemble.py`;
existing projects still use `transplant.py`.

## Success criteria

1. `workflow/harvest/INVENTORY.json` exists and every row has `class` in
   CORE | OPTIONAL | IDENTITY | CANDIDATE | NEVER.
2. `workflow/harvest/pack/MANIFEST.json` lists only CORE + OPTIONAL paths that exist
   in this repo (no Pokemon tree, no cg, no kaggle.json, no humanizer).
3. `python scripts/onboard_check.py` and `python scripts/sabotage_test.py` still pass.
4. `scripts/transplant.py` PORTABLE_FILES is a subset of CORE (not expanded without a
   named incident).
5. `python workflow/harvest/pack/assemble.py --check` exits 0; CORE matches
   `transplant.PORTABLE_FILES`; inventory counts match rows.
6. Greenfield smoke: assemble into a temp git repo; target `onboard_check.py` exits 0.
   (`sabotage_test.py` stays a source-repo guard: a fresh dest has no git HEAD, so it
   cannot yet act as a transplant source.)
7. `workflow/harvest/IDEAS.md` + `IDEAS.json` exist; every idea has family + encode;
   JSON row count matches the markdown tables.

## Assumption registry

- Assumption: The factory is a transplantable protocol, not the union of campaign tools.
  Source: LAWS.md meta-law; DECISIONS 2026-08-08 skeleton size; playbook TOOLS.md sprawl note
  Status: holding
  | Affects: Phase 1 NEVER list

- Assumption: Identity files (START-HERE, AGENTS, GATES contents, CLAIMS, PLAN) must not
  copy live from this repo into a target.
  Source: transplant.py docstring
  Status: verified (code + assemble.py identity templates)
  | Affects: pack layout

- Assumption: A first-pass 36-row inventory was enough "everything that can be repurposed."
  Source: harvest Phase 1 v1, 2026-08-23
  Status: invalidated (2026-08-23) — expanded to 93 *files*, which was still the wrong object.
  | Affects: Phase 1 completeness

- Assumption: The harvest object is portable *files* (CORE/OPTIONAL/CANDIDATE/NEVER paths).
  Source: harvest Phase 1 goal
  Status: invalidated (2026-08-23) — principal: "take all of the valuable development ideas that
  were used DURING the project"; "growing evolving factory"; file inventory was trees not forest.
  Evidence: playbook eight load-bearing ideas, EVAL_PROTOCOL, DEAD-ENDS scope guards,
  START-HERE field facts, Law 1–9.
  | Affects: Phase 1 (files remain substrate), Phase 2 (ideas ledger is the product)

- Assumption: If a dollar price is hard to quote, the harvest has little value.
  Source: 2026-08-23 valuation reply (sale price of git files is the wrong lens; rejected)
  Status: invalidated (2026-08-23) — replacement cost of the *ideas* is the campaign tuition
  (thousands of human hours). Sale price of git files is the wrong lens.
  | Affects: how value is stated in IDEAS.md

## Phasing

### Phase 1 — File pack  [status: done]
**Produces:** INVENTORY.json/md, pack/README.md, pack/MANIFEST.json, identity templates,
candidate extracts, assemble.py
**Verifies:** success criteria 1–6
**Note:** necessary substrate; not the harvest the principal asked for.

### Phase 2 — Development-ideas ledger  [status: done]
**Produces:** `workflow/harvest/IDEAS.md` + `IDEAS.json` (145 ideas across 10 families)
**Verifies:** success criterion 7; onboard_check still green after START-HERE path add

### Phase 3 — Optional module installers  [status: pending]
*(coarse)* `transplant.py --extra comms|ops` after sabotage fixtures exist per extra.
**Produces:** extra allowlists; does not grow default PORTABLE_FILES

### Phase 4 — Blueprint factory (Miracle pattern)  [status: done]
**Produces:** `workflow/blueprint/` capability catalog, EXTRACT-LOG, orient/bootstrap/selftest,
fleet+method templates
**Verifies:** `python workflow/blueprint/bin/selftest.py`; onboard_check; sabotage_test

### Pivot — 2026-08-23
What flipped: harvest object is *ideas used during the project*, not files to copy.
Decision: absorb the file pack as Phase 1 (encoding substrate); make the ideas ledger
Phase 2 and the factory's growing core. Do not import the mill. Value stated as tuition
already paid + tuition avoided, not as a SKU price.
Recommend: resume at Phase 3 only if an extra is needed; otherwise the factory grows by
adding idea rows when the next project hits an incident.

## Research

- `playbook/TOOLS.md` (Pokemon) — already a generalized tool inventory
- `playbook/RULES-LEDGER.md` — UNIV / FLEET / PROJ port column
- `scripts/transplant.py` — current CORE
- `workflow/blueprint/ARCHITECTURE.md` — six-layer target
- `workflow/harvest/pack/candidate/UNIV-RULES.md` — UNIV extract
- `workflow/harvest/pack/candidate/TOOL-REBUILD.md` — rebuild triggers
