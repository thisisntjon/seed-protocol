# Throughput is not progress

**A pinned case study of 1,979 agent-landed pull requests in a single-operator fleet**

Authors: measurement run 2026-08-24 (Bonkers factory) · **author-run, not independently reproduced**
Object: `thisisntjon/poketcg` @ `9522a8a37078d00f46b99a586b825b789b01387d`
Pre-registration: `workflow/experiments/2026-08-24-pr-case-study.md`
Artifacts: `artifacts/summary.json`, `sample80_summary.json`, `pr_join.json`, `review_sample.json`

---

## Abstract

Empirical SE now has *breadth* on agent pull requests: Watanabe et al. study 567 Claude Code PRs across 157 projects (83.8% merged); MSR 2026 mining-challenge papers use tens of thousands of agent PRs to taxonomize communication and human intervention. Those papers answer whether agent PRs are accepted.

They do not answer what happens when **one human operates ~100 git identities for six weeks** and treats GitHub as a factory. We census that regime.

On a pinned first-parent history, **1,979** PR-linked commits cover **84.6%** of 2,338 GitHub-merged PRs. **43.2%** change only `.md`/`.txt`. **39.7%** have churn &lt; 100. The week with the most landings (652) was **58.4% docs-only**; a later week with 79 landings was **6.3% docs-only and 77.2% code**. Throughput and construction moved in opposite directions.

GitHub cannot recover the fleet: squash authors are 1,974×`thisisntjon` + 5×`ash`; `shortlog --all` still shows 103 seat names. In a seeded review sample of 40, independent human GitHub review is **0/40** (16 Codex-bot reviews; 1 human login is the PR author).

A stratified 80-PR inspection (oversampling code) found **2** PRs that changed the playing agent. Protocol ledgers barely cite PRs (`playbook/RULES-LEDGER.md`: 3 census PRs); the kanban cites 301. Incident→check is not visible as a GitHub join.

**Contribution.** A rerunnable, pinned negative: in this factory, PR count, seat count, and GitHub reviews are invalid proxies for verified product progress. Complementary to merge-rate papers as **depth plus mechanism**.

---

## 1. Introduction

From 2026-07-09 a public GitHub repository was used as the coordination substrate for a Kaggle Pokémon TCG agent campaign. The operating theory, later captured as a playbook, was that agent seats would claim work by pushing branches, merge via pull requests, and accumulate verified improvement. The same campaign independently recorded a stretch of **high PR volume with few closed experimental loops** (Law 8 in the distilled protocol).

Two stories are available.

**Story A — volume.** ~2,300 merged PRs, ~100 git authors, ~50 PRs per day. Agents work.

**Story B — conveyor.** Most landings are documentation, board, or measurement receipts. Identity collapses at squash. Reviewers on GitHub are bots or the owner. The playing agent almost never moves.

Story A is what a mining paper sees if it stops at `is:merged`. This paper tests Story B with a pre-registered instrument.

---

## 2. Related work

Watanabe, Li, Kashiwa, Reid, Iida, Hassan, arXiv:2509.14745v3: 567 Claude Code PRs, 157 projects, 83.8% accepted, 54.9% merged unmodified. Question: *are agent PRs useful to maintainers?*

MSR 2026 mining challenge / AIDev follow-ons (~33k agent PRs): description quality, human intervention (guidance vs decision vs code change), test mocking. Question: *population regularities across tools.*

This study is **n = 1 repository, n = 1 principal**. That blocks treatment-effect claims. It enables claims those datasets cannot make: a written incident→rule protocol, a second mainline stream that is **not** a PR (mailbox/lead/master pushes), and a time series in which documentation share **falls** as volume falls.

We do not claim a higher merge rate. We claim a **different estimand**: composition and identity, not acceptance.

---

## 3. Methods

### 3.1 Object

```
git fetch origin
origin/main = 9522a8a37078d00f46b99a586b825b789b01387d
# 2026-08-24T11:29:23-07:00
```

Local clone: `C:\Users\thisi\Desktop\Pokemon`. GitHub: `gh api search/issues` the same calendar day.

### 3.2 PR-linked commits

First-parent log. Linked iff subject matches `\(#N\)\s*$` or `Merge pull request #N`. Files and churn from `git log --numstat`.

**Kill bar (pre-registered):** file list for &lt;80% of GitHub-merged PRs → INVALID-INSTRUMENT. Observed coverage **1,979 / 2,338 = 84.6%**. Instrument stands. The 15.4% gap is not imputed.

**Bound:** if every missing GitHub-merged PR were `has_code`, docs-only on the full 2,338 would still be **855/2,338 = 36.6%**. The qualitative claim survives the gap.

### 3.3 File-shape labels (pass 0, N=1,979)

See `CODEBOOK.md`. `docs_only` = every path is `.md` or `.txt`. `has_code` = at least one `.py`/`.go`/`.js`/`.ts`/`.rs`/`.java`/`.c`/`.cpp`/`.h`. `small` = additions+deletions &lt; 100.

These labels describe **bytes**, not value. A 49-line conformance audit can be load-bearing.

### 3.4 Intent labels (pass 1 auto, pass 2 inspection, n=80)

Stratified draw: 20 `docs_only` + 20 `has_code` + 20 `other` + 20 extra `small`, hashed on pin+PR. **Oversamples code** relative to the population (population `has_code` 38.5%). Product-share estimates from this sample are therefore **upper bounds** on population product share.

Pass 1: keyword+path rules (`label_sample.py`).
Pass 2: exclusive human inspection of subject+paths (`pass2_labels.py`):

| Label | Meaning |
|---|---|
| PRODUCT | playing agent or ship payload |
| INSTRUMENT | harness / eval / test / guard |
| EVIDENCE | analysis receipt, measurement JSON, verify writeup |
| GOVERNANCE | board, inbox, proposal, design, writeup, onboarding |
| CEREMONY | cycle log, index bump, changelog, bus rotation |
| OTHER | empty merge, unclassifiable |

Exact agreement pass1 vs pass2: **50/80 = 62.5%**. Pass 1 over-called EVIDENCE (keyword “gate/bank”). Pass 2 is the reported intent distribution. This is **one inspector**, not dual independent coders. That is a threat, not a hiding place.

### 3.5 Reviews

SHA-256(pin ∥ PR) order; first 40 of the PR-linked index; `GET /pulls/{n}/reviews`. Human := login without `bot`, `codex`, `copilot`.

### 3.6 Protocol join

Regex `#(\d{1,4})` in `workflow/`, `playbook/`, `ptcg-agent/docs/`, intersected with census PR numbers.

---

## 4. Results

### 4.1 GitHub volume

| | N |
|---|---|
| All PRs | 2,935 |
| Merged | 2,338 |
| Closed unmerged | 585 (20% of closed) |
| Open | 12 |
| Calendar days (repo created 2026-07-09 → pin) | 46 |

Naive rate ≈ 51 merged PRs/day. Section 4.3 is why that sentence is not a result.

### 4.2 Composition (N=1,979 PR-linked first-parent commits)

| Class | N | Rate | Prior lore (~2026-08-16) |
|---|---|---|---|
| docs_only | 855 | **43.2%** | 44.7% |
| has_code | 761 | 38.5% | — |
| other | 362 | 18.3% | — |
| churn &lt; 100 | 786 | **39.7%** | 39.6% |

**The 44.7% / 39.6% figures reproduce.** They were not campaign mythology.

Churn is heavy-tailed: p50=146, p90=1,349, p99=8,879, max=135,280. Means of “lines per PR” are not estimands.

Class tokens in **squash subjects**: 11 `[ops]`, 9 `[research]`, 0 `[bank]`/`[instrument]`. GitHub *title* search still finds `[bank]`=148. **The protocol token does not survive `git log`.** Tools that mine commits will not see it.

Squash authors: `thisisntjon` 1,974; `ash` 5.

### 4.3 Time series — the firehose was documentation

Week of 2026-07-08:

| Week starting | N | docs-only | has_code |
|---|---|---|---|
| 2026-07-08 | 652 | **58.4%** | 29.8% |
| 2026-07-15 | 488 | 45.7% | 28.5% |
| 2026-07-22 | 68 | 20.6% | 55.9% |
| 2026-07-29 | 571 | 34.2% | 48.5% |
| 2026-08-05 | 87 | 37.9% | 40.2% |
| 2026-08-12 | 79 | **6.3%** | **77.2%** |
| 2026-08-19 | 34 | 11.8% | 50.0% |

Peak day in this instrument: **2026-07-10, 279** PR-linked commits. (Campaign prose sometimes says 353; different population; not used here.)

**The highest-volume week is the worst code-share week.** When volume fell by an order of magnitude, code share rose. That is the measurable form of “throughput is not progress.”

### 4.4 Identity (RQ3)

| Surface | Unique names |
|---|---|
| `git shortlog -sn --all` | 103 |
| `git log origin/main --pretty=%an` | 19 |
| PR-linked squash commits | **2** |
| GitHub login (review sample) | **1** (`thisisntjon`) |

Seat names (Ash, Misty, Roach, 5080, …) are real as **protocol**. They are erased at squash and never present on `pulls[].user`. A miner using GitHub identity reports a solo developer. Both sentences can be true.

### 4.5 GitHub reviews (RQ2)

n=40 seeded PR-linked merges:

| | Count |
|---|---|
| Any review | 17/40 |
| `chatgpt-codex-connector[bot]` | 16 |
| Human login | 1 — `thisisntjon` (the author) |
| Independent human, not author | **0/40** |

Clopper-Pearson 95% interval on 0/40: **0–8.8%**. We reject “GitHub reviews are the verifier channel.” We do not reject the existence of off-GitHub verification (receipts, second-seat git authors on branches). Those traces are **not this graph**.

Doctrine was author XOR verifier, including across hardware. **GitHub cannot operationalize that doctrine** once squash + owner-login are the public objects.

### 4.6 Main is not only PRs

First-parent commits at the pin: **4,093**. PR-linked: 1,979. **2,106** have no PR token. Prefix counts on the no-token remainder (before merge-message absorption): mailbox, lead/board, master/control dominate.

Playbook rule: `main` is lead-write-only. Git shape: the lead **pushed** inbox and board updates. “2,338 merged PRs” undercounts governance traffic and, if used as a construction count, overcounts product.

### 4.7 Intent sample (n=80, code-oversampled)

Pass-2 distribution:

| Intent | N | Share of sample |
|---|---|---|
| EVIDENCE | 29 | 36.3% |
| GOVERNANCE | 26 | 32.5% |
| INSTRUMENT | 15 | 18.8% |
| CEREMONY | 4 | 5.0% |
| OTHER | 4 | 5.0% |
| **PRODUCT** | **2** | **2.5%** |

The two PRODUCT PRs: **#113** (deck-aware archetype selection in `agent/config.py` + `heuristic.py`) and **#1423** (`rules_lucario.py`, 2-line churn, “decode fidelity, not strength”).

Governance+ceremony = **30/80**. Evidence receipts = **29/80**. Playing-agent edits = **2/80**.

Because the sample **oversampled** `has_code`, 2.5% PRODUCT is an **upper-ish** glimpse of population product share, not a lower bound. Even in the code stratum, most Python is harness/eval (INSTRUMENT), not the agent.

### 4.8 Protocol join — incident→check is not a PR foreign key

| Surface | Census PR numbers cited |
|---|---|
| `workflow/` tree (any md/json/py) | 1,230 / 1,979 (**62%**) |
| of which `workflow/KANBAN.md` | **301** |
| `workflow/DECISIONS.md` | 226 |
| `workflow/GATES.md` | **46** |
| `playbook/RULES-LEDGER.md` | **3** |
| `playbook/PLAYBOOK.md` | **0** |
| `workflow/DEAD-ENDS.md` | 5 |
| `ptcg-agent/docs/EVAL_PROTOCOL.md` | 5 |

Most “joins” are the **board mentioning PRs**, which is what a board is for. The **rules ledger that claims every rule names an incident** cites three census PRs. The playbook narrative cites zero. **You cannot recover incident→check rates from GitHub or from the playbook’s own PR references.** Measuring that rate needs a different instrument (receipt tables with a `pr` field), which this campaign mostly did not keep.

---

## 5. What a paper may claim

**May claim (author-run, this pin):**

1. Docs-only 43.2% and small-PR 39.7% on N=1,979; prior 44.7%/39.6% reproduce.
2. Volume and code-share moved inversely across weeks.
3. GitHub user and squash author collapse to the owner; 103 seat names live only off `main`.
4. 0/40 independent human GitHub reviews in a seeded sample.
5. In a code-oversampled 80, 2 PRs changed the playing agent.
6. Rules-ledger PR join is essentially empty (3); kanban join is dense (301).

**May not claim:**

- Encoded rules never failed again (unmeasured; Bonkers DECISIONS already flags the header).
- 103 independent agents.
- Merge volume ⇒ product progress.
- Causal benefit of the protocol vs a bare repo (still HYPOTHESIS).
- External validity beyond this factory.

---

## 6. Threats to validity

1. **Single operator, single repo, competition.** Mechanism, not ATE.
2. **Coverage 84.6%.** Bound in §3.2: docs-only ≥ 36.6% even in the adversarial fill.
3. **`docs_only` ≠ waste.** Playbook capture is markdown. The veto is on *volume as strength*, not on writing docs.
4. **One inspector on n=80.** Pass1/pass2 exact agreement 62.5%. A second coder could move PRODUCT by a few PRs; they cannot move it to a majority given the file-shape census.
5. **Author-run census.** Independent rerun of `measure_pr_census.py` on the same SHA is the next scientific bar.
6. **Squash erases co-authors.** By design of the merge policy under study.
7. **Keyword join `#1234` collides with issue numbers and hashes.** We intersect with the census set, which removes most false positives, not all (short numbers).

---

## 7. Why this paper has value

The 2025–2026 agent-PR literature is answering **acceptance**. This factory is a warning about **instrumentation**. If the next lab mines GitHub for “agent productivity,” this case is a documented way that dashboard goes up while the product stands still: docs-majority firehose, identity collapse, bot reviews, harness code mistaken for agent code, protocol tokens that do not survive squash.

That is citable. It is not a medal.

Recommended venue: arXiv cs.SE, then ICSE SEIP / FSE industry / MSR *experience*. Do not submit as a clone of Watanabe. Cite them as the breadth baseline and state the estimand difference in paragraph two.

---

## 8. Reproduce

```text
git -C <poketcg> fetch origin
git -C <poketcg> rev-parse origin/main
# pin used here: 9522a8a37078d00f46b99a586b825b789b01387d
python measure_pr_census.py <poketcg> --no-reviews
python postprocess.py
python label_sample.py
python pass2_labels.py
python join_mentions.py
```

Cite the pin, not live HEAD. New merges will move rates; that is expected.

---

## 9. Factory implication (Bonkers)

Keep CORE sabotage and identity-by-hash. Do not treat squash-to-owner as harmless. H1–H7 (CI bind, bootstrap fixture, measurement tripwires) exist because GitHub will not tell the truth by default.

Do not print 2,338 or 103 in a pitch. Print **43.2% docs-only (N=1,979, SHA 9522a8a…)** and **2/80 PRODUCT in a code-oversampled sample**.
