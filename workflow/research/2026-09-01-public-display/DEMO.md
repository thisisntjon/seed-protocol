# DEMO — judge-runnable path (T-003)

Proposal only. Does not implement Python. Does not edit `verify.yml` or
`workflow/blueprint/bin/`. Does not require `C:\Users\thisi\Desktop\Pokemon`,
`poketcg`, a second harness, or network after `git clone` of **this** repo.

**Kill bar:** if a step on the “judge runs this” list cannot be executed on a
fresh Ubuntu/Windows checkout of this repository alone, rewrite that step. A
screenshot is not a demo.

H1 is already bound in CI: `selftest.py` → `check_catalog()` fails if a
capability README is deleted. H2 (bootstrap dest + dest-poison) is **not**
in `selftest.py` today — specify it here for a later builder; do not run it
as the judge demo.

---

## 1. Judge clone path (this repo only)

Preconditions: Python 3.11+ (CI matrix is 3.11 / 3.12), `git`, stdlib only.
Working directory = clone root. No `pip install`. No extra remotes.

```text
git clone <this-repo-url> thefleet
cd thefleet
python scripts/onboard_check.py
python scripts/sabotage_test.py
python scripts/poc_check.py
python workflow/blueprint/bin/selftest.py
python workflow/harvest/pack/assemble.py --check
python workflow/blueprint/bin/orient.py
```

Same six commands as `.github/workflows/verify.yml` and the current README
Reproduce block. Order matches CI. Paths are all in this tree.

| Command | Pass token (stdout) | Exit |
|---|---|---|
| `python scripts/onboard_check.py` | `ONBOARD CHECK PASSED` | 0 |
| `python scripts/sabotage_test.py` | `SABOTAGE TEST 18/18 PASSED` | 0 |
| `python scripts/poc_check.py` | `PASS` lines; no `AssertionError` | 0 |
| `python workflow/blueprint/bin/selftest.py` | `BLUEPRINT SELFTEST PASSED` | 0 |
| `python workflow/harvest/pack/assemble.py --check` | `PACK CHECK PASSED` | 0 |
| `python workflow/blueprint/bin/orient.py` | `THE WHOLE JOB` and `NEXT:` | 0 |

What this proves: docs match the tree (onboard); the checker fails seeded
defects (sabotage / Law 2); POC scorers are calibrated (poc_check); catalog
READMEs + ENCODED ledger paths exist and orient is not decorative
(`check_catalog`, `check_ledger`, `check_orient_clean`,
`check_orient_sabotage`); the harvest pack matches disk (`assemble --check`);
cold-start prints state from files (`orient.py`).

What this does **not** prove: C-004, a treatment effect, or that bootstrap
`--dest` is a CI fixture (H2 still TODO).

Green onboard ≠ answered research question.

---

## 2. Dest-poison fixture (add later — not the judge list)

H2 (`workflow/blueprint/HARDENING.md`): `selftest.py` creates a temp git
repo, runs `bootstrap.py --dest`, then dest `onboard_check.py` and dest
`orient.py`. Fail if either is green-without-START-HERE or red-when-complete.

`bootstrap.py` (no `--dest`) only verifies this repo has the factory tree.
`--dest PATH` requires an **existing standalone git repo with a clean
working tree** (`transplant.target_is_clean_git`), then assemble CORE +
identity templates and copy the blueprint tree. Dest gets
`scripts/onboard_check.py` and a template `START-HERE.md`. Receipt
`workflow/receipts/2026-08-23-harvest-pack.md` already recorded dest
onboard exit 0 after greenfield assemble — encode that, do not re-prove it
by hand.

Existing `check_orient_sabotage()` is **not** H2: it points `orient.py` at
an empty temp dir that only has `README.md`. It never calls `bootstrap.py`
and never runs dest onboard.

### Add these two functions to `workflow/blueprint/bin/selftest.py`

Call both from `main()` after the four existing checks. Do not change
`verify.yml` (it already runs `selftest.py`).

**`check_bootstrap_roundtrip()`** — complete dest is green.

1. `tempfile.mkdtemp(prefix="blueprint-dest-")`
2. `git init` in that directory (no commit required; tree must be empty/clean)
3. `python workflow/blueprint/bin/bootstrap.py --dest <tmp>` — expect exit 0
4. `python <tmp>/scripts/onboard_check.py --root <tmp>` — expect exit 0
5. `python workflow/blueprint/bin/orient.py --root <tmp>` — expect exit 0
6. `shutil.rmtree` in `finally`

Fail strings: dest onboard red-when-complete; dest orient red-when-complete;
bootstrap non-zero. That is the H2 “assemble or identity templates broken”
kill.

**`check_dest_poison()`** — Law 2 on the dest front door.

1. Same setup as `check_bootstrap_roundtrip` (or share one temp dest)
2. After dest is green: `Path.rename` dest `START-HERE.md` → `START-HERE.md.bak`
   (do not invent a fake path row; missing front door is the defect)
3. Dest onboard: `python <tmp>/scripts/onboard_check.py --root <tmp>` — expect
   **non-zero** (onboard already fails with
   `START-HERE.md missing -- the skeleton has no front door`)
4. Dest orient: `python workflow/blueprint/bin/orient.py --root <tmp>` — expect
   **non-zero** (`REFUSED: START-HERE.md missing at --root`)
5. Restore: rename `.bak` back to `START-HERE.md`
6. Dest onboard and dest orient — expect exit 0
7. `rmtree` in `finally`

Fail if dest onboard stays 0 with START-HERE gone (guard decorative) or
stays non-zero after restore.

Do **not** put `C:\Users\thisi\Desktop\Pokemon` or poketcg in either
function. Dest is a throwaway git repo on the runner.

Until these land, H2 is still a receipt, not a fixture. The judge list in
§1 stays green without them.

---

## 3. README figure spec (one chart, data already in this tree)

Do not rerun the census to draw this. Plot from the checked-in weekly dict.
`docs_only_rate` is the campaign headline; the figure is the weekly mix.

**Source file:** `workflow/research/2026-08-24-pr-case-study/artifacts/summary.json`

**Headline rate (same file, not a weekly key):** `docs_only_rate` = **0.432**
(`docs_only` 855 / `n_first_parent_pr_commits` 1979).

**Series (each week object):** `docs_only`, `has_code`, `n`.
Do not stack `docs_only` + `has_code` as if they sum to `n` — `other`
(and one `empty` in week `2026-07-15`) make up the remainder. Plot three
separate series. Optional fourth series `other` is out of this spec.

**Weekly values (copy from `summary.json` → `weekly`):**

| Week start (`weekly` key) | `docs_only` | `has_code` | `n` |
|---|---:|---:|---:|
| 2026-07-08 | 381 | 194 | 652 |
| 2026-07-15 | 223 | 139 | 488 |
| 2026-07-22 | 14 | 38 | 68 |
| 2026-07-29 | 195 | 277 | 571 |
| 2026-08-05 | 33 | 35 | 87 |
| 2026-08-12 | 5 | 61 | 79 |
| 2026-08-19 | 4 | 17 | 34 |

**Title:** Weekly file-shape mix of PR-linked commits (poketcg pin)

**X-axis:** Week start date (ISO date; keys are Wednesdays) — unit: calendar week

**Y-axis:** PR-linked first-parent commits — unit: commits per week

**Marks:** grouped bars or three lines, one per series (`docs_only`,
`has_code`, `n`). Legend uses those exact key names.

**Source caption (print under the figure):**

> Source: `workflow/research/2026-08-24-pr-case-study/artifacts/summary.json`
> field `weekly`. Object: `thisisntjon/poketcg` @ pin
> `9522a8a37078d00f46b99a586b825b789b01387d`. Labels: `docs_only` = every
> changed path is `.md`/`.txt`; `has_code` = at least one `.py`/`.go`/`.js`/
> `.ts`/`.rs`/`.java`/`.c`/`.cpp`/`.h`; `n` = PR-linked first-parent commits
> that week (`CODEBOOK.md`). Campaign `docs_only_rate` = 0.432 (855/1979).
> Author-run, not independently reproduced. The clone that produced the
> census is not this repository.

The figure is demoable from this repo because the JSON is in the tree. A
judge who only clones thefleet can redraw it; they cannot regenerate it.

---

## 4. Not demoable without poketcg or a second harness

| Wanted demo | Why it is not on the judge list |
|---|---|
| Census **rerun** | `measure_pr_census.py <poketcg>` needs the pinned poketcg clone (`PAPER.md` §8). That path is not this repo. Independent science-grade PASS is still `BLOCKED_ON` that rerun (`workflow/receipts/2026-08-24-pr-case-study.md`). |
| `switch.py` | Does not exist. H8 / ARCHITECTURE / C03 PARTIAL. Continuity hole. Do not invent a paste-block stand-in as a judge command. |
| Fleet **mailbox** | No `workflow/mailbox/` in this tree. Mailbox is opt-in / deferred (`ARCHITECTURE.md`; PLAN assumption: MVS is solo + two agents; mailbox is out of the public object). Needs a second seat writing `INBOX-<name>.md` on origin/main. |
| Vendor switch / second harness | Same as `switch.py`: no escrow, no adapter render, no `--to claude\|codex`. Orient on this checkout is one harness reading files. |
| Pokemon operating loop | poll → claim-by-push → verdict PR → bus receipt is poketcg mill, not this clone. |
| C-004 ablation | Designed and paused; spend-gated. Not a demo. |

Judge-visible substitute for the census: read `PAPER.md` + `artifacts/summary.json`
and (later) the §3 figure. That is consumption of a pinned artifact, not a
rerun.

---

## Builder note (not a judge step)

Smallest later change that turns CI red if bootstrap is broken:
implement `check_bootstrap_roundtrip` + `check_dest_poison` in
`selftest.py` only. H1 already reds a deleted capability README.
Do not grow `PORTABLE_FILES`. Do not import the mill.
