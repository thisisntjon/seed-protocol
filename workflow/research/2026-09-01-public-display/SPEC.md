# SPEC — recommended public-display version

Synthesis of T-001–T-005. Does not implement `README.md` or `verify.yml`.
Does not flip visibility (`GATES.md` publication). C-004 stays **HYPOTHESIS**.
Author of this file is the lead session; a later session must review it
(author XOR).

## Recommended object

The public entry is **Bonkers / SEED**: a measurement protocol a stranger can
name in one sentence, run in six commands, and score as an *instrument*. The
GitHub slug `thefleet` stays; the first sentence says fleet orchestration is
deferred. The interesting result is an author-run composition census whose
public dataset is `artifacts/` in this repo (`poketcg` is private). The factory
bins stay runnable. The mill, VoiceCraft, valuation memos, and a default-fleet
mailbox do not appear. After the CHANGE list is applied and `JUDGES.md` plus
the README figure land, a methodology panel can honestly sit in the high 80s.
A mixed panel tops out below 100 until someone who is not the author reruns
the census or C-004. That remainder is not a documentation problem.

## ADD

| Path | Why |
|---|---|
| `JUDGES.md` | T-001: score the instrument, not C-004. 90-second path: this file → README Abstract–Limitations → `CLAIMS.md` → `python scripts/onboard_check.py`. |
| README figure (in `README.md` Evidence section) | T-003: weekly `docs_only` / `has_code` / `n` from `artifacts/summary.json` field `weekly`. Title, axes, caption as DEMO.md §3. |
| `workflow/blueprint/bin/selftest.py` functions `check_bootstrap_roundtrip` and `check_dest_poison` | T-003 / H2. Later build board. Not a judge-visible file add; CI already runs selftest. |
| `workflow/research/2026-08-24-pr-case-study/check_artifacts.py` (optional, small) | T-004: jsonl line count vs `summary.n_first_parent_pr_commits`. Weaker than a rerun; label it so. |

No new capability READMEs. No harvest idea rows. No mailbox.

## CHANGE

| Path | Change |
|---|---|
| `README.md` | First sentence from FRONT-DOOR. H2 order: Abstract → Research question → Limitations → claims → evidence (incl. figure) → reproduce → tree map. Remove “(private)” and the “repository is private” limitation line when a human answers the publication gate. Name `artifacts/` as the public dataset in the same paragraph as `thisisntjon/poketcg`. |
| GitHub About | `Bonkers (SEED): a measurement protocol for agentic software work — not a fleet.` |
| `LAWS.md` Law 9 | Drop `~$49,686`. Keep the law. Do not invent a substitute dollar (HYGIENE). |
| `scripts/spend_check.py` | Drop the dollar from the docstring; do not default the meter to `Path.home() / ".claude" / …`. |
| `workflow/blueprint/HARDENING.md` + `PLAN.md` | Rewrite `$120k` / `$30k` / `$70k` / `$20k` as “replacement-cost memo, no dollar.” Or omit HARDENING from the landing page (SCOPE KEEP-IN-TREE). |
| `workflow/blueprint/ARCHITECTURE.md`, `workflow/PLAN.md`, `workflow/handoffs/2026-08-08-p1-complete.md` | Delete `claude.ai/code/artifact/…` URLs; cite in-repo files only. |
| Case-study `PAPER.md`, `REPORT.md`, `measure_pr_census.py`, `label_sample.py`, `join_mentions.py`, experiment pre-reg | Remove `C:\Users\thisi\Desktop\Pokemon` defaults. Require an explicit clone argument. |
| `workflow/harvest/INVENTORY.json` `sources[]` | Strip to logical names (`poketcg/playbook`, `user-skills`) or omit the file from the landing page. |
| `workflow/canon/DECISIONS.md` | “Private remote” row: rewrite when visibility flips. Keep the 2026-08-18 Law-9 caveat row. First-name `Jon` → “principal” on files that remain featured. |
| `START-HERE.md` | Keep as machine door. Leave poketcg / thebus URLs only with the existing retired/not-this-repo caveat. |

## OMIT (from the landing page and from any public “what you get” list)

Per SCOPE EXCLUDE (24) and KEEP-IN-TREE. Do not commit if still untracked:

- VoiceCraft (`web/`, `humanizer_*.py`, 2026-08-13 receipts)
- `seed.md`, `valueproject.md`, pipeline `.docx`, `Multi-Harness-Coordination-Blueprint.md`, `Fleet/`
- Pokemon harness mill, GitHub-issue bus, default-fleet mailbox
- `SLOP_RETRACTIONS.md`, `workflow/relay/beliefs/`
- Investigation `board/` tickets and this `2026-09-01-public-display/` folder as featured docs
- HARDENING dollar lede if not rewritten — do not feature the memo

Relay (`scripts/relay.py` + profiles): **keep in git** (`assemble --check`). **Hide from README.**

## Estimated score after this SPEC is implemented

| Panel | Now | After SPEC (Wave A + JUDGES + figure + hygiene) | After H2 dest-poison in CI (Wave B) | Reason |
|---|---:|---:|---:|---|
| Mixed contest | 47 | **72** | **84** | Identity tax and screenshot dollars go away; they still cannot rerun the census or watch a second harness. |
| Methodology track | 59 | **82** | **88** | Instrument + public artifacts + honest badge. 100 needs a non-author census rerun or an opened research extract. |

These are lead estimates, not measurements. A later session may revise them.
Do not print 47 or 72 on the public README (HYGIENE: internal scores are omit-from-public-view).

## Unbuyable remainder

What still cannot be 100 after every row above:

1. **Independent census.** `poketcg` is private. Artifact arithmetic (T-004) is not Law 4. Opening the mill to a panel, or publishing a path-free PR extract, is a human gate.
2. **C-004.** Unrun. A polished instrument is not a treatment effect. Running P3 underpowered and calling it 100 is a fail.
3. **C-003 dest in this repo.** Human Delta is another machine. H2 makes *factory* bootstrap a fixture; it does not replay that transplant.
4. **`switch.py` / second harness.** Specified as not demoable (T-003). Building it is Wave B continuity, not a front-door file.
5. **Author XOR on this SPEC.** The session that wrote it does not get to grade it as 100.

If the contest scores treatment effect, stop at “instrument” on the badge and accept a ceiling below 90. If it scores methodology, implement CHANGE + ADD, then H2, then ask a different model to onboard from `JUDGES.md` alone.

## Builder order (later board, not this file)

1. Hygiene rewrites that a judge would screenshot (README private line, Law-9 dollar, HARDENING lede, desktop paths in the paper/scripts, claude.ai URLs).
2. `JUDGES.md` + README outline + weekly figure.
3. H2 dest-poison in `selftest.py`.
4. Optional `check_artifacts.py`.
5. Human: publication gate, then About line.

Do not start a fleet mailbox, a capability-catalog tour, or a valuation pass to “look more complete.”

## Dissent

- SCOPE INCLUDE is 35 paths; the working tree is larger. Featured set ≠ git set. T-006 keeps that split.
- HYGIENE lists 85 rows including board tickets. Those tickets should not ship as display; they do not block the public object if `board/` is unfeatured.
- DEMO leaves dest-poison off the judge list until H2 lands. SPEC agrees: do not advertise a command that is not in CI.

## Checks

`python scripts/onboard_check.py` must still exit 0 after this file exists (no new START-HERE path claims required).
