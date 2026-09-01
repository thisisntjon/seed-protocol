# Throughput is not progress

**Status:** ARCHIVE as the short census memo. The camera-ready case study is
[`PAPER.md`](PAPER.md) (adds n=80 intent labels, protocol join, coverage bound).
Do not cite this file as the full result.

**A measured case study of agent-authored pull requests in a single-operator fleet**

**Status:** MEASURED (author-run) · **Not independently reproduced**
**Pin:** `thisisntjon/poketcg` `origin/main` `9522a8a37078d00f46b99a586b825b789b01387d` (2026-08-24)
**Instrument:** `measure_pr_census.py` · artifacts in `artifacts/summary.json`
**Pre-registration:** `workflow/experiments/2026-08-24-pr-case-study.md`

---

## Abstract

Public empirical work on agent-authored pull requests now has breadth: hundreds of Claude Code PRs across many repos, and mining-challenge datasets of tens of thousands of agent PRs. Those papers answer *whether agent PRs merge*. They do not answer what happens when **one human operates ~100 agent identities for six weeks** and treats GitHub as a factory conveyor.

We census the first-parent history of `thisisntjon/poketcg` at a pinned SHA. Among **1,979** PR-linked commits (84.6% of 2,338 GitHub-merged PRs):

- **43.2%** change only `.md`/`.txt` files (prior lore 44.7% — reproduced within 2pp).
- **39.7%** have churn &lt; 100 lines (prior lore 39.6% — reproduced).
- **38.5%** touch a conventional source suffix (`.py` and kin).
- Squash authors on those commits: **1,974 `thisisntjon` / 5 `ash`**.
- `git shortlog --all`: **103** author names (agent seats).
- Seeded GitHub review sample **n=40**: 17 have any review; **16 are a Codex bot**; **1 human login is the PR author**. Independent human GitHub review: **0/40**.

Volume peaked in week one (652 PR-linked commits, **58.4% docs-only**) and collapsed by late August (34 in the last week, **11.8% docs-only**, 50% code). The mix improved as the firehose slowed. That is the opposite of “more PRs ⇒ more product.”

**A valuable paper exists.** It is not “we merged 2,300 agent PRs.” It is: *in this extreme single-operator regime, PR count, seat count, and GitHub review graphs are invalid proxies for verified improvement; identity collapses at squash time; author-XOR-verifier cannot be recovered from GitHub; and a large share of mainline traffic never was a PR (mailbox/lead/master direct pushes).* Complementary to Watanabe et al. (breadth) as **depth plus negatives**.

---

## 1. Question

**RQ1.** Of PR-shaped landings on `main`, what fraction are documentation-only or small?

**RQ2.** Can GitHub’s PR graph recover independent verification (author XOR verifier)?

**RQ3.** Is “2,300 merged PRs / 100 authors” a valid description of who did the work?

**RQ4.** Did the docs-only share stay constant, or did it fall as volume fell?

We pre-registered the instrument and a kill bar: if we could not list files for 80% of GitHub-merged PRs, stop and call INVALID-INSTRUMENT. We do not pre-register a “pass” for a product claim. The census **is** the result.

---

## 2. Related work (why this is not another merge-rate paper)

Watanabe et al., arXiv:2509.14745 (v3, 2026-02): **567** Claude Code PRs across **157** projects; 83.8% accepted; 54.9% merged without further modification. Question: usefulness and acceptance in the wild.

MSR 2026 mining challenge and follow-ons (AIDev-scale, 33k+ agent PRs): communication, human intervention taxonomies, over-mocked tests. Question: *population* regularities.

This corpus is **n=1 repository, n=1 principal**. That is a weakness for generalization and a strength for mechanism. We have: a written incident→rule ledger, sabotage-before-trust as doctrine, a documented inversion of local eval vs live ladder, and a first-parent history that is mostly squash commits plus a second stream of **non-PR** mainline governance. Mining-challenge datasets do not contain that protocol layer.

---

## 3. Methods

**Object.** `git fetch origin`; `origin/main` = `9522a8a37078d00f46b99a586b825b789b01387d`.

**PR-linked commits.** First-parent log. A commit is PR-linked if the subject matches `\(#N\)\s*$` (squash) or `Merge pull request #N` (merge commit). File list and churn from `git log --numstat`.

**GitHub totals.** `gh api search/issues` at measurement time (same day as the pin).

**Reviews.** SHA-256(pin ∥ PR number) order; first 40 PR-linked rows; `GET /pulls/{n}/reviews`. “Human” := login not containing `bot`, `codex`, or `copilot`.

**Codebook.** `CODEBOOK.md`. Labels are file-shape, not “this PR was ceremony.”

**Coverage bar.** 1,979 / 2,338 = **84.6%** ≥ 80% → instrument stands. The missing 15.4% are GitHub-merged PRs that did not appear as first-parent subjects with a PR token (rebase/squash message variance, or not on this first-parent path). We do **not** impute them.

**Not this run.** Dual-coder labeling of construction vs ceremony; join of each PR to a GATES/receipt row; recurrence of encoded rules. Those remain the next measurement, not claims.

---

## 4. Results

### 4.1 GitHub volume (live search)

| State | N |
|---|---|
| All PRs | 2,935 |
| Merged | 2,338 |
| Closed unmerged | 585 (20.0% of closed) |
| Open | 12 |

Repo created 2026-07-09. Calendar span to pin: **46 days**. Merged PRs / calendar day ≈ 51 if you ignore weekends; that headline is what we are about to disqualify.

### 4.2 Composition of PR-linked first-parent commits (N=1,979)

| Class | N | Rate |
|---|---|---|
| `docs_only` (.md/.txt only) | 855 | **43.2%** |
| `has_code` (has .py/etc.) | 761 | 38.5% |
| `other` (json/yml/csv/assets) | 362 | 18.3% |
| empty | 1 | |
| churn &lt; 100 | 786 | **39.7%** |

Prior Write-Up figures: **44.7% docs-only, 39.6% under 100 lines** (census date ~2026-08-16, ~2,293 merged). This rerun, on a later pin and a slightly different PR-token rule, lands **43.2% / 39.7%**. The lore numbers were not a hallucination. They also were not a law of nature: see §4.3.

Churn is heavy-tailed: median 146; p90 1,349; p99 8,879; max 135,280. A mean “lines per PR” would be a lie.

Class tokens in **squash subjects** are almost unused: 11 `[ops]`, 9 `[research]`, 0 `[bank]`/`[instrument]` of 1,979. GitHub *search* on PR **titles** still finds `[bank]`=148 because **the GitHub title is not the squash subject**. Protocol that lives only in GitHub titles does not survive `git log`. That is an operational finding, not a nit.

### 4.3 Time: the firehose was documentation; later weeks were code

Week buckets from first PR-linked day 2026-07-08:

| Week of | N | docs-only | has_code |
|---|---|---|---|
| 2026-07-08 | 652 | **58.4%** | 29.8% |
| 2026-07-15 | 488 | 45.7% | 28.5% |
| 2026-07-22 | 68 | 20.6% | 55.9% |
| 2026-07-29 | 571 | 34.2% | 48.5% |
| 2026-08-05 | 87 | 37.9% | 40.2% |
| 2026-08-12 | 79 | 6.3% | **77.2%** |
| 2026-08-19 | 34 | 11.8% | 50.0% |

Peak **day** in this instrument: **2026-07-10, 279** PR-linked commits (campaign lore said 353 — different population; we do not overwrite it, we do not cite 353 from this pin).

Read the table as a single sentence: **the week with the most PRs was the worst week for code share.** When daily volume fell by an order of magnitude, the code share rose. Throughput and construction moved in opposite directions.

### 4.4 Identity collapse (RQ3)

| Surface | Unique names |
|---|---|
| `git shortlog -sn --all` | **103** |
| `git log origin/main --pretty=%an` | 19 |
| Squash/PR-linked commits in this census | **2** (`thisisntjon` 1,974; `ash` 5) |
| GitHub `user.login` on review sample | **1** (`thisisntjon`) |

The 103 names are real as *seat protocol* (Ash, Misty, Roach, 5080, …). They are **not** recoverable from GitHub PRs or from squash commits on `main`. Attribution-is-seat is doctrine; squash-to-owner is practice. Any mining paper that uses `pulls[].user` on this repo will report a single author.

### 4.5 GitHub reviews do not implement author XOR verifier (RQ2)

Seeded **n=40** PR-linked merges:

| | N / 40 |
|---|---|
| Any review | 17 |
| Codex connector bot | 16 of those 17 |
| Human login | 1 — and it is `thisisntjon` |
| Independent human, not the PR author | **0** |

95% binomial interval on 0/40 independent human reviews: **0–8.8%**. We do not claim “never.” We claim GitHub review is **not the verifier channel** in this sample. Verifiers, if they existed, left traces in git authors on branches, receipts, or bus comments — not in `pulls/reviews`.

### 4.6 Main is not only PRs

First-parent commits at the pin: **4,093**. PR-linked: 1,979. **2,106** have no PR token. Among no-token subjects (separate prefix count on the same log): mailbox ~348, lead/board ~462, master/control ~701, plus merge-message leftovers now absorbed. Direct-to-main **governance** (inbox, board, MASTER) is a first-class stream. “2,338 merged PRs” undercounts what the lead wrote to `main` and overcounts product construction if you treat every merge as a feature.

This is the playbook rule “`main` is lead-write-only” visible as git shape: the lead did not open PRs for mailbox updates; they pushed.

---

## 5. What this supports, and what it does not

**Supported (this run, author-only):**

1. Docs-only and small-PR rates on PR-linked first-parent history are ~43% and ~40% (N=1,979). Prior 44.7% / 39.6% **reproduce**.
2. Early high-volume weeks were docs-majority; later low-volume weeks were code-majority.
3. GitHub identity and squash identity collapse to the owner.
4. GitHub reviews in a 40-PR sample are bot-or-self; they do not implement XOR-verifier.
5. A large first-parent stream is not a PR at all.

**Not supported:**

- “Encoded rules never failed again” (no recurrence column; not measured here).
- “The fleet was 103 independent agents” (103 git names, one GitHub user, one principal).
- “2,338 merges ⇒ verified product progress” (contradicted by §4.2–4.3 and by the campaign’s own Law 8).
- Causal benefit of the protocol vs a bare repo (Bonkers C-004 still HYPOTHESIS).
- Generalization to other orgs (n=1).

**Examples (illustrative, not a coded 200-row sample):**

- Docs-only: #9 strategy evidence ledger; #1081 cold-start docs catch-up; #2108 conformance-audit amendments (tiny, load-bearing).
- Has-code: #1 board status linter; #896 eval raw-opponent fail-close; #1981 identity predicate drop.
- Other: #3 ladder log CSV; #1437 harvest tranche JSONL.

#2106-class work (conformance audit, +49 / 1 file) is the reminder that **bytes are not importance**. File-shape rates describe the conveyor, not the value of a given merge.

---

## 6. Threats

1. **n=1 human, n=1 repo, competition incentives.** External validity is limited. The paper’s job is mechanism, not a treatment effect.
2. **Coverage 84.6%.** 15% of GitHub-merged PRs are not in this first-parent PR-token set. If those missing PRs were all code, docs-only on the *full* merged set could fall. Bound: even if all 359 missing were `has_code`, docs-only ≥ 855/2338 = **36.6%**. The qualitative claim survives.
3. **`docs_only` is not “waste.”** Some markdown PRs are the playbook. The rate is still a veto on using *volume* as strength.
4. **Review sample n=40.** Enough to reject “GitHub reviews are the verifier channel.” Not enough to estimate bot-review prevalence tightly (17/40 = 43%, CI wide).
5. **Author-run.** Independent reproduction of `measure_pr_census.py` on the same SHA is required before this is a non-author PASS.
6. **Squash erases co-authors.** Seat handles exist on branches (`git shortlog --all`). Main does not keep them.

---

## 7. The highest-value paper (what to publish)

**Title (working):** *Throughput is not progress: a single-operator multi-agent PR factory, measured.*

**Venue:** arXiv cs.SE immediately; then ICSE SEIP / FSE industry / MSR **experience**. Do not send this as a mining-challenge clone of Watanabe. Their N is broader. Ours is a **protocol autopsy**.

**Contribution, three sentences:**

1. We publish a pinned, rerunnable census showing that in this factory, merge volume and seat count are invalid productivity metrics (docs-only ~43%, identity collapse, 0/40 independent GitHub reviews).
2. We show a time signature: documentation-majority firehose, then fewer PRs with higher code share — the campaign’s own “ceremony pathology” as a plot, not an anecdote.
3. We show that the interesting verifier protocol (author XOR verifier, sabotage, frozen bars) **does not appear in the GitHub review graph** and must be recovered from git authors, receipts, and checkers — or it will be invisible to the next empirical study that only mines `pulls`.

**What still has to happen for a journal-grade version (not this file):**

- Non-author rerun of the script.
- Dual-coded sample (even 100 PRs) of construction / governance / evidence / ceremony, published codebook.
- Join: PR → receipt/GATES row → check landed in the same cycle (the playbook’s “incident→check” claim, currently unverified as a rate).

Without those, this report is the **highest-value version we can honestly ship today**: measured, pinned, reproducible by a second machine, scoped, and already strong enough to kill the wrong paper.

---

## 8. What this does for the factory (Bonkers)

This measurement is why CORE includes sabotage and identity-by-hash, why squash-to-owner is a **threat** not a convenience, and why H1–H7 (CI bind, bootstrap fixture, measurement tripwires) raise expected value: they make the *next* repo’s GitHub graph less of a lie.

Do not put 2,338 or 103 in a marketing sentence. Put **43.2% docs-only (N=1,979, pin SHA)** and **0/40 independent GitHub reviews**.

---

## Reproduce

```text
git -C C:\Users\thisi\Desktop\Pokemon fetch origin
git -C C:\Users\thisi\Desktop\Pokemon rev-parse origin/main
# expect 9522a8a37078d00f46b99a586b825b789b01387d at the time of this report
python workflow/research/2026-08-24-pr-case-study/measure_pr_census.py C:\Users\thisi\Desktop\Pokemon --no-reviews
python workflow/research/2026-08-24-pr-case-study/postprocess.py
```

Compare `artifacts/summary.json` `docs_only_rate` and `small_rate` to this text. Drift after new merges is expected; cite the pin, not the live HEAD.
