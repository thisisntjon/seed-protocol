# EVIDENCE — what a public judge can check (T-004)

Investigation brief only. Does not edit `CLAIMS.md`. Does not flip visibility
(`GATES.md` item 2, publication). **No new SUPPORTED rows.**

Read with: `CLAIMS.md`, `pocs/POC-REGISTRY.json`,
`workflow/research/2026-08-24-pr-case-study/PAPER.md` (§ abstract + §3 methods),
`workflow/experiments/2026-08-24-pr-case-study.md`,
`workflow/research/2026-08-24-pr-case-study/artifacts/`.

---

## 1. poketcg is private; the public dataset is `artifacts/`

`thisisntjon/poketcg` is **PRIVATE** (`gh repo view` → `isPrivate` true, confirmed
2026-08-31; ticket T-004; PLAN assumption registry). It is not a public object.
A stranger cannot fetch the pin, rerun `measure_pr_census.py`, or re-query that
repo’s GitHub search/review API.

The public-in-this-repo dataset is:

`workflow/research/2026-08-24-pr-case-study/artifacts/`

Eight files (2026-09-01 inventory):

| File | Role |
|---|---|
| `summary.json` | Rolled-up census + identity + weekly + churn + nested GitHub/review headers |
| `pr_index.jsonl` | One object per first-parent PR-linked commit (the 1,979-row census) |
| `github_totals.json` | Four GitHub search integers from measurement day |
| `review_sample.json` | Seeded n=40 review rows + header counts |
| `sample80_pass1.jsonl` | Stratified 80, keyword/path intent |
| `sample80_pass2.jsonl` | Same 80 plus one-inspector pass-2 intent |
| `sample80_summary.json` | Pass-1/pass-2 tallies and 50/80 agreement |
| `pr_join.json` | Protocol-tree `#N` join against the census PR set |

Scripts, codebook, paper, and pre-registration live beside that directory. They
describe the instrument; they do not substitute for the private clone.

**Reproduce-the-census caveat.** `PAPER.md` §8 and `README.md` say a reader can
rerun the instrument against pin
`9522a8a37078d00f46b99a586b825b789b01387d`. That path needs a poketcg checkout
the public tree does not contain. What this repo can offer a second reader is
**artifact-internal consistency**, which is weaker than a full rerun (see §4).

---

## 2. What each artifact file can and cannot show alone

“From that file alone” means: no sibling artifacts, no poketcg clone, no `gh`
against the private repo.

| Artifact | A second reader can check from that file alone | They cannot check from that file alone |
|---|---|---|
| `summary.json` | That these keys exist and are self-quoting: `pin_sha`, `n_first_parent_pr_commits` (1979), `n_first_parent_skipped_no_pr_token` (2106), `docs_only` / `docs_only_rate`, `small_lt_100` / `small_rate`, `has_code`, `other_files`, `empty`, `file_class`, `title_class`, `squash_authors`, `unique_authors_origin_main_log`, `unique_authors_shortlog_all`, `shortlog_all_names` (103 strings), `n_days_with_pr`, `peak_day`, `peak_day_n`, `mean_pr_per_active_day`, `github`, `review_sample`, `github_merged_coverage`, `weekly`, `churn`, `direct_main_not_pr_token`. That `docs_only / n` = 0.432, `small_lt_100 / n` = 0.3972, `1979 / github.pr_merged` = 0.8464. That `file_class` sums to 1979. That `review_sample.independent_human_not_author` is stored as 0. | That the pin exists or that git/gh produced these numbers. That `file_class` / `small` follow `CODEBOOK.md` (no paths). That 103 `shortlog_all_names` came from `git shortlog -sn --all`, or that 19 authors exist on all of `origin/main`. That the 2,106 no-token first-parent commits exist. That GitHub totals were live. Treatment effect of SEED. |
| `pr_index.jsonl` | Object count; unique `pr` count; keys per row (`pr`, `sha`, `when`, `author`, `subject`, `churn`, `n_files`, `file_class`, `title_class`, `small`). Tallies of `file_class`, `small`, `author`, `title_class`. Recompute Wednesday-aligned weekly mix, peak day, active-day count, mean, and churn percentiles using `postprocess.py` (`ch[int(q * (n-1))]`). | That each `sha` is a real first-parent commit on the pin. That `file_class` is correct (no path list). That subjects match git. Coverage vs GitHub-merged (no denominator). Identity off `main`. Reviews. Intent. Protocol join. |
| `github_totals.json` | That the four integers are `pr_all` 2935, `pr_merged` 2338, `pr_closed_unmerged` 585, `pr_open` 12, and that 585+12+2338 = 2935. | The search queries, calendar day, or that GitHub still answers these counts. Coverage (needs the 1979). Anything about file shape. |
| `review_sample.json` | Header keys `k`, `with_any_review`, `with_human_review`, `review_logins`; that `rows` has 40 objects; that 17 rows have `n_reviews` > 0 and 1 row has `human_reviewer` true (PR 2377, login `thisisntjon`). That every `gh_user` in-file is `thisisntjon`. | That GitHub `/pulls/{n}/reviews` returned these logins (private repo). That the 40 PRs are the SHA-256(pin ∥ PR) prefix named in `PAPER.md` §3.5. Independent-human = 0 as a *header field* (that field lives on `summary.json`, not here). File-shape truth of those PRs. |
| `sample80_pass1.jsonl` | 80 objects; keys include `pr`, `sha`, `file_class`, `paths_head`, `pass1_intent`; tally of pass-1 labels. | That the draw is the registered 20+20+20+20 hash sample. That `paths_head` is complete or that pass-1 rules were applied correctly (`label_sample.py` needs the rows). Population rates (sample is code-oversampled; file says so only in `sample80_summary.json`). |
| `sample80_pass2.jsonl` | 80 objects; `pass2_intent` tally; `exact_agree` count 50. The two `PRODUCT` rows are PR 113 and PR 1423 (subjects in-file). | That pass-2 labels are right (one inspector; `PAPER.md` §3.4). Playing-agent bytes in the private tree. A second coder. Dual-independent coding. |
| `sample80_summary.json` | `n` 80; `pass2` / `pass1` maps; `exact_agree` 50 and `exact_agree_rate` 0.625; `product_or_instrument` 17; `governance_or_ceremony` 30; `evidence` 29; the note that the sample is stratified, not SRS. | That those maps match the jsonl (needs the jsonl). That 2.5% PRODUCT is a population rate (the note forbids that). |
| `pr_join.json` | Keys `census_n` 1979, `cited_in_protocol_tree` 1230, `cite_rate` 0.6215, `by_root`, `top_files`, `special` (e.g. `playbook/RULES-LEDGER.md` `in_census` 3; `workflow/KANBAN.md` 301 via `top_files`), `uncited` 749. Arithmetic: 1230+749 = 1979. | That the regex join on poketcg `workflow/` / `playbook/` / `ptcg-agent/docs/` produced these hits (`join_mentions.py` needs the private trees). That `#N` tokens are PRs not issues. Incident→check rates. |

Sibling-file checks (still **not** a rerun): `github_totals.json` equals
`summary.json` → `github`; every `review_sample.json` row’s `pr` / `file_class` /
`churn` / `title_class` joins `pr_index.jsonl`; every sample-80 `pr` is in the
index. Those joins are available in this tree. They still do not prove the
private git/gh objects.

---

## 3. Strongest honest public claim

Instrument + author-run composition. Not a treatment effect. Not a new
`CLAIMS.md` row.

> A public reader of this repository may say only that a pre-registered,
> author-run first-parent census instrument (not independently reproduced;
> source repo private) released 1,979 PR-linked rows at pin
> `9522a8a37078d00f46b99a586b825b789b01387d` with 43.2% docs-only and 39.7%
> churn &lt; 100 — composition of that instrument, not a SEED treatment effect
> and not an independently reproduced scientific PASS.

Bound to:

- Pre-registration and OUTCOME: `workflow/experiments/2026-08-24-pr-case-study.md`
  (PASS = instrument ran; coverage 1979/2338 = 84.6% ≥ 80% kill bar;
  `INDEPENDENT_REPRO: not yet`).
- Methods: `PAPER.md` §3 (file-shape labels describe bytes, not value;
  n=80 oversamples `has_code`; one inspector).
- What a paper may claim / may not: `PAPER.md` §5 (n=1 factory; no ATE;
  C-004 stays HYPOTHESIS).
- Existing claim table: `CLAIMS.md` C-004 remains **HYPOTHESIS**. This brief
  does not add or upgrade a row.

`PAPER.md` contribution language (“rerunnable, pinned negative”) is honest
**for an author who holds the private clone**. It is not a public-judge
reproduce story. Do not print 2,338 or 103 as the public headline
(`PAPER.md` §9).

---

## 4. Minimum extra artifact for 1,979-row internal consistency

**None.** `pr_index.jsonl` is already the row file.

A second reader, without a Pokemon clone, can:

1. Count JSON objects in `pr_index.jsonl` and compare to
   `summary.json` → `n_first_parent_pr_commits`.
2. Tally `file_class`, `small`, `author`, `title_class` and compare to
   `docs_only` / `has_code` / `other_files` / `empty`, `small_lt_100`,
   `squash_authors`, `title_class`.
3. Recompute `weekly`, `peak_day`, `n_days_with_pr`, `churn` from `when` /
   `churn` using `postprocess.py`.

T-004 investigator check (2026-09-01, this session): 1,979 objects; unique
`pr` = 1,979; file-shape / small / squash-author / title-class / weekly /
peak-day (2026-07-10, 279) / rates match `summary.json`. That is **artifact
arithmetic**, not Law 4 independent reproduction.

**Weaker than a full rerun.** Internal consistency cannot: walk first-parent
history at the pin; re-apply `CODEBOOK.md` to changed paths; recover the 2,106
no-token commits; confirm GitHub totals or reviews; or move the experiment
from author-run to independently reproduced.

A *stronger* public check (not required for the minimum above) would be a
per-commit path list so a reader could re-derive `file_class` / `small` from
the codebook without the clone. That file is not in `artifacts/` today
(`pr_index.jsonl` stores `n_files` and the already-applied label). Adding it
is still not a git rerun.

---

## 5. What still requires the author

These are not public-judge closeouts. They do not create SUPPORTED rows.

### Independent paper reproduction

`workflow/experiments/2026-08-24-pr-case-study.md` requires a non-author
rerun of `measure_pr_census.py` against
`9522a8a37078d00f46b99a586b825b789b01387d` before citing the census as a
non-author scientific PASS. That needs the private poketcg object and, for
the review sample, `gh` against that repo (owner-authenticated on measurement
day). Artifact-internal consistency does not discharge this bar.

### C-003 / Human Delta machine

`CLAIMS.md` C-003 is already **SUPPORTED** for the tested transplant. Evidence
is `workflow/receipts/2026-08-08-p2c-cold-v3-pass.md` (Human Delta target
`2ff86b509c120f4070c41493a0745baf1f74c6d1`; POC-01 / POC-06). The dest is
**not** a tree in this repository. A public judge can read the receipt and
`workflow/measurements/2026-08-08-p2c-independent-cold-*-v3.json`. They
cannot reproduce the transplant or the cold-start session without the
author’s Human Delta machine/checkout. This brief does not re-litigate or
extend C-003.

### P3 / C-004

`CLAIMS.md` C-004 stays **HYPOTHESIS**. `pocs/POC-REGISTRY.json` POC-09
(bare-versus-SEED) is **ACTIVE**, `progress_percent` 15. Pre-registration
`workflow/experiments/2026-08-08-p3-bare-vs-seed-ablation.md` is
**PENDING — EXECUTION HOLD** (stale treatment object; not priced; independent
repro required for any PASS). A public display must not narrate causal
benefit. Author (or a later gated board) owns corpus, pricing, execution,
and blinded analysis.

### Also author-bound (not claim upgrades)

| Need | Why a stranger with only this repo fails |
|---|---|
| Pass-2 second coder | One inspector; 62.5% pass-1/pass-2 agreement (`PAPER.md` §3.4, §6.4) |
| Protocol join rerun | `pr_join.json` is a dump of private markdown/json trees |
| `shortlog --all` = 103 | Names are listed; git proof is on the private object |
| 2,106 no-token mainline commits | Count only; no companion jsonl |
| GitHub live totals / reviews | Private API surface |
| POC-10 public thermometer | `TODO` in `POC-REGISTRY.json`; this brief is input, not that surface |
| Visibility flip | `GATES.md` item 2 — human only |

---

## 6. What this repo already allows a judge to verify (not this paper)

In-tree instrument calibration, distinct from the poketcg census:

| ID | Status | Public-in-this-repo evidence | Public judge cannot |
|---|---|---|---|
| C-001 | SUPPORTED | `workflow/receipts/2026-08-08-verified-progress-control.md` | — (re-run status surface here) |
| C-002 | SUPPORTED | same receipt; `scripts/sabotage_test.py` | — (re-run sabotage here) |
| C-003 | SUPPORTED | P2c receipt + cold-score JSON | Reproduce against Human Delta dest |
| C-004 | HYPOTHESIS | P3 experiment file | Invent a benefit |
| C-005 | SUPPORTED | `workflow/receipts/2026-08-08-p2a-invalid-transplant.md` | — (negative was banked) |
| POC-01, 02, 04, 05, 06, 07 | DONE | registry paths | Treat DONE as C-004 |
| POC-03, 08, 10 | TODO | named `missing` fields | Treat as shipped |
| POC-09 | ACTIVE 15% | P3 hold | Run or “complete” P3 |

`RETRACTIONS.md` (checked 2026-09-01) has no row retracting 1979 / 43.2% /
39.7% / 0/40 / 2/80. Cite those only as author-run artifact numbers with the
pin and the private-source caveat.

---

## 7. Fence

- Do not claim poketcg is public.
- Do not claim the census is independently reproduced.
- Do not claim C-004 or a treatment effect.
- Do not add `CLAIMS.md` rows.
- Internal consistency ≠ rerun.
- Publication of any of this to an audience remains `GATES.md` item 2.
