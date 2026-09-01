# Harden the recovered $120k — ten moves

**Stamped:** 2026-08-23
**Triage:** Light. No mill import, no fleet mailbox, no P3 spend, no PORTABLE_FILES growth.
**Plan:** `PLAN.md` (this directory). SEED `workflow/PLAN.md` stays paused.

The $120k is cost-to-recreate portable yield ($30k executable + $70k named mistakes +
$20k expected avoided waste). It expires if CI does not bind it, if bootstrap is only a
story, and if measurement rules stay prose. These ten items lock that value in **this
repo**. Each is reversible, stdlib, and done when a command is green.

Skip on purpose: Pokémon harness mill, thebus, answer-map YAML as default, `queue_worker`,
growing default transplant, any dollar spend.

---

## H1 — Bind the factory in CI

**Hardens:** $30k executable (rot)
**Risk:** trivial. Add three lines to `.github/workflows/verify.yml`.
**Do:** run `workflow/blueprint/bin/selftest.py`, `workflow/harvest/pack/assemble.py --check`,
`workflow/blueprint/bin/orient.py` on every push, same job as onboard/sabotage.
**Done when:** a PR that deletes a capability README turns CI red.
**Status:** wired 2026-08-31 — `verify.yml` runs selftest, assemble --check, and orient on every push. Confirm on the first GitHub Actions run.
**Why first:** an unbound catalog is a museum. This is how Miracle’s tests protect deliverables.

## H2 — Bootstrap round-trip inside selftest

**Hardens:** $30k install path
**Risk:** low. Temp git, already proven by hand; encode Law 2.
**Do:** `selftest.py` creates a temp repo, runs `bootstrap.py --dest`, then dest
`onboard_check.py` and dest `orient.py`. Fail if either is green-without-START-HERE (already)
or red-when-complete.
**Done when:** breaking assemble or identity templates fails selftest without touching Pokémon.
**Why:** C-003 is SUPPORTED for transplant; the *factory* bootstrap is only a receipt. Make it
a fixture.

## H3 — Append-only factory ledger

**Hardens:** $70k inspectability (Miracle run ledger, lite)
**Risk:** low. One jsonl, size-capped, no second source of truth for PLAN.
**Do:** `workflow/blueprint/events.jsonl`. `orient.py`, `selftest.py`, `bootstrap.py` append
one JSON object: ts, tool, sha, exit. Receipts already live in `workflow/receipts/`; do not
duplicate them. Cap file (e.g. last 500 lines) so it cannot become a novel.
**Done when:** a selftest run adds a line; wiping PLAN is still illegal — events are grep
fuel, not status.
**Why:** “the repo is the memory” fails if tool runs leave no artifact. This is Miracle
`workflow_runs` without SQLite.

## H4 — Three frozen recipes (composition without a DAG)

**Hardens:** $20k option (use, not admire)
**Risk:** low. Markdown + JSON. No graph runner.
**Do:** `workflow/blueprint/recipes/`

| Recipe | Steps |
|---|---|
| `greenfield.v1` | git init → bootstrap --dest → fill four lines → orient → onboard |
| `incident.v1` | write idea row → encode check → sabotage fixture → receipt |
| `promotion.v1` | freeze EXPERIMENT.md on main → run → independent verify → bank or KILL |

**Done when:** each recipe has a README answering the five Miracle questions and a
`--dry-run` that prints the commands without executing spend.
**Why:** Miracle escaped “a pile of tools” by composing them. We are still a pile of
capabilities. Recipes are the cheapest compose layer.

## H5 — Path-free copies of two skills

**Hardens:** $30k+$70k portability (second machine)
**Risk:** low. Copy markdown; strip `C:\Users\thisi`.
**Do:** `workflow/blueprint/skills/phased/` and `skills/handoff/` from `~/.claude/skills`,
with helpers invoked as `python skills/handoff/handoff.py` relative to the repo. Do **not**
copy peek, godot, comfy, grail.
**Done when:** grep of those copies finds no `C:\Users\thisi`. `orient.py` can point at them.
**Why:** `master-skills-catalog.md` already marked this as the porting failure. The factory
that only works on this desktop is not recovered value.

## H6 — Spend and approval as objects

**Hardens:** $20k + C12 (empty COST.md checkboxes)
**Risk:** low. Templates only. No API keys, no auto-spend.
**Do:** `templates/BUDGET.md` (window, loops-closed, $/closed-loop, source = principal
note — never invent cash). `templates/APPROVAL.json` (id, what, irreversible class,
status, sha). Optional: `spend_check.py` reads BUDGET.md if present, skips if absent.
**Done when:** a project can record “we spent X, closed Y loops” without a spreadsheet, and
a missing BUDGET is not a red onboard (optional extra).
**Why:** Miracle’s approval/budget objects are how spend becomes inspectable. Pokémon only
had prose. Do not cite unverified Law-9 dollars.

## H7 — Three measurement tripwires, with sabotage

**Hardens:** $70k C-family (the expensive mistakes)
**Risk:** low if scoped to *this* repo’s receipts and START-HERE. Law 2 required.
**Do:** `scripts/measure_guard.py` (or `blueprint/bin/measure_guard.py`):

1. **Skipped ≠ pass** — any tool that prints PASS must also print ran/skipped counts;
   selftest already has a cousin; extend to `poc_check` style or a wrapper used by
   selftest.
2. **Ship-path list** — `workflow/blueprint/SWITCHES.json`: named capabilities and
   `on`/`off`. Guard fails if START-HERE claims a bin that SWITCHES marks off.
3. **Receipt identity** — new receipts in `workflow/receipts/` must have EXACT_REF that is
   either a git sha that exists or a labeled working-tree token (already partially
   checked). Add: no bare “PASS” without an EVIDENCE path in backticks that exists.

**Done when:** sabotage_test (or selftest) has three red fixtures, one per tripwire.
**Why:** markdown EVAL-DISCIPLINE will not fire. These three would have caught skip-bot
preflight, dormant switches, and bus-comment “evidence.”

## H8 — `switch.py`: escrow + paste block

**Hardens:** original unused pain (usage limit / vendor change) — $30k continuity gap
**Risk:** low-medium. Git refs only; no push; no hook install by default.
**Do:** `bin/switch.py --to claude|codex`. If dirty: `git stash push -u` or commit to
`refs/factory/escrow/<utc>` locally. Print a paste-ready boot: read START-HERE, run
orient, do not trust chat. Do **not** build full adapter render yet.
**Done when:** selftest in a dirty copy shows escrow ref exists and working tree can be
restored; `--to` unknown vendor exits 2.
**Why:** ARCHITECTURE listed this as the layer poketcg lacked. A paste block is 80% of the
value of adapters.

## H9 — `conventions.yml` as the single source

**Hardens:** C06 adapters without a renderer
**Risk:** low. One YAML file. Render can wait.
**Do:** `workflow/blueprint/harness/conventions.yml` listing: four-line job, orient command,
GATES SLA hours, verdict tokens, identity files never copied, NEVER mill paths.
`selftest.py` asserts AGENTS.md and START-HERE mention the orient command (string check),
so conventions cannot drift silently forever.
**Done when:** changing the orient path in conventions without START-HERE fails selftest
**or** a documented allow-list says “render not built; check is advisory.” Prefer fail.
**Why:** vendor switch re-teaches by hand today. One file is the adapter substrate.

## H10 — Short handoff + factory claim

**Hardens:** I-A10 health metric + C-003 for the *factory*, not just CORE
**Risk:** trivial.
**Do:** write `workflow/handoffs/2026-08-23.md` (must be shorter than
`2026-08-08-p1-complete.md`). Add CLAIMS **C-006**: “`bootstrap.py --dest` on a clean git
repo yields onboard_check 0 and orient 0 without domain imports.” Status SUPPORTED, bound
to H2 fixture once H2 lands (until then HYPOTHESIS).
**Done when:** onboard_check still green; newest handoff is the 08-23 file; C-006 has a
bound path after H2.
**Why:** a factory whose last handoff is the skeleton era is not cold-start ready. Claims
are how we stop repeating “portable” without a falsifier.

---

## Sequence (do in order; each is its own receipt)

H1 → H2 → H3 → H7 are the **lock**. They turn $120k from a memo into CI.
H4 → H5 → H6 are **use**. They make the next project able to consume it.
H8 → H9 are **continuity**. They close the poketcg hole.
H10 can run parallel with H1 (handoff now; C-006 after H2).

## Explicitly not these ten

P3 bare-vs-SEED ablation (spend, not low risk). Fleet mailbox. Answer-map as day-0.
Growing `transplant.py` PORTABLE_FILES. Importing Miracle’s media graph runner.
