# HYGIENE — public landmines (T-002)

Investigator inventory of the **git-tracked** tree only. Does not rewrite landmines.
Does not flip visibility (`GATES.md` item 2). No commit.

Ignored as instructed (untracked / not in `git ls-files`): `web/`, `scripts/humanizer_*.py`,
`seed.md`, `Fleet/` (0 tracked files), `valueproject.md`, VoiceCraft receipts, and other
untracked mill.

`git ls-files` count at inventory time: **182** paths. HEAD: `b41ed67e61e8eb010496f2d91ee2abd6914c701c`.

## Method

`git grep` searches the index (tracked files) by default. Equivalent to
`git grep … $(git ls-files)` without expanding 182 paths on the Windows command line.

Commands actually run (pattern as passed to `git grep`; PowerShell string literals):

| # | command | line hits | files |
|---|---|---|---|
| G1 | `git grep -I -n "C:\\Users\\thisi"` | **15** | 11 |
| G2 | `git grep -I -n "C:/Users/thisi"` | **7** | 2 |
| G3 | `git grep -I -n -E "C:[/\\]Users[/\\]thisi"` (union of G1∪G2) | **22** | 13 |
| G4 | `git grep -I -n "claude.ai/code/artifact"` | **5** | 4 |
| G5 | `git grep -I -n "claude.ai"` | **6** | 4 |
| G6 | `git grep -I -n "120k"` | **9** | 3 |
| G7 | `git grep -I -n "$120k"` (same 9 lines; `$` is not extra) | **9** | 3 |
| G8 | `git grep -I -n "120,000"` | **0** | 0 |
| G9 | `git grep -I -n "49,686"` | **6** | 4 |
| G10 | `git grep -I -n "49686"` | **0** | 0 |
| G11 | `git grep -I -n "private" -- README.md` | **2** | 1 |
| G12 | `git grep -I -n -w "Jon" -- "*.md" "*.py"` | **21** | 7 |
| G13 | `git grep -I -n "~/.claude"` | **18** | 5 |
| G14 | `git ls-files` | — | **182** |

Ticket-stated equivalent of G1: `git grep -I -n "C:\\Users\\thisi" $(git ls-files)` → **15** rows.
Forward-slash desktop paths (`C:/Users/thisi`) are a separate 7 and are inventoried below.
G6 = every committed `$120k` / `120k` hit (9). G9 = every committed `49,686` hit (6). Each of
those 15 token-hits has its own table row.

HARDENING’s `$120k` is a **replacement-cost memo** (cost-to-recreate portable yield:
`$30k` executable + `$70k` named mistakes + `$20k` expected avoided waste). It is not cash
earned, not a sale price, and not independently metered. A judge will still screenshot the
dollar. Say that in every `$120k` why-cell.

`49,686` is **not** in `workflow/canon/RETRACTIONS.md`. `DECISIONS.md` (2026-08-18) marks it
an open verification item: two audits report the figure does not appear in the source
project, and `playbook/COST.md` dollar cells were empty checkboxes. Law 6: do not invent a
replacement dollar. Retract the token or drop it; do not substitute a new figure.

## Actions (allowed values only)

| action | meaning here |
|---|---|
| rewrite-in-place | Keep the file in the public object; change the token |
| retract-token | Remove via the retractions ledger; do not cite a substitute number |
| omit-from-public-view | File/section is not part of the public-display object |
| leave-with-caveat | Token may remain if the caveat is adjacent and a screenshot still cannot be misread |

## Inventory

Columns: path | token/class | recommended action | why a judge would screenshot it.

**Total rows: 85.**

| path | token/class | recommended action | why a judge would screenshot it |
|---|---|---|---|
| `board/tickets/T-001.md` | `C:\Users\thisi\Desktop\thefleet` | omit-from-public-view | Local Windows username + desktop layout; maps GitHub `thefleet` to a home directory |
| `board/tickets/T-001.md` | `C:\Users\thisi\Desktop\Pokemon\START-HERE.md` | omit-from-public-view | Names a second private product on the same desktop; PTCG mill adjacency |
| `board/tickets/T-001.md` | leftover-private + `47/100` | omit-from-public-view | “README still says private” plus an internal contest score a panel did not publish |
| `board/tickets/T-002.md` | `C:\Users\thisi` | omit-from-public-view | Repeats the desktop-username token; board is operational, not display |
| `board/tickets/T-002.md` | `claude.ai` artifact URLs (class mention) | omit-from-public-view | Points judges at session-private Claude artifacts as if they were citations |
| `board/tickets/T-002.md` | `claude.ai/code/artifact/` | omit-from-public-view | Same class; names the URL prefix a judge would search |
| `board/tickets/T-002.md` | `$120k` (known-hits list) | omit-from-public-view | Investigation ticket repeating the replacement-cost dollar as a search key |
| `board/tickets/T-002.md` | `49,686` (known-hits list) | omit-from-public-view | Investigation ticket repeating the unverified Law-9 dollar as a search key |
| `board/tickets/T-002.md` | `$120k` (acceptance line) | omit-from-public-view | Acceptance criterion names `$120k`; a crop looks like a banked valuation. **Replacement-cost memo, not cash** |
| `board/tickets/T-002.md` | `49,686` (acceptance line) | omit-from-public-view | Same line also names `49,686`; second required token-hit. Unverified Law-9 dollar |
| `board/tickets/T-002.md` | `$120k` (HARDENING memo note) | omit-from-public-view | Third `$120k` hit on the ticket; still a replacement-cost memo, board should not ship |
| `board/tickets/T-004.md` | `thisisntjon/poketcg` (private) | omit-from-public-view | Confirms a second repo is private while this tree cites it as the case-study source |
| `board/tickets/T-004.md` | `gh repo view` → private (2026-08-31) | omit-from-public-view | Timestamped privacy of the evidence repo; looks like hidden data |
| `board/tickets/T-005.md` | `C:\Users\thisi\Desktop\Pokemon\playbook\BOOTSTRAP.md` | omit-from-public-view | Desktop path into the private mill’s playbook |
| `README.md` | `(private)` on the GitHub line | rewrite-in-place | Front door says the repo is private; a public contest screenshot is a contradiction |
| `README.md` | “This GitHub repository is private. Private backup is not public publication.” | rewrite-in-place | Limitations section advertises secrecy; judges will crop it as “they did not mean to publish” |
| `README.md` | `thisisntjon/poketcg` as case-study source | leave-with-caveat | Private evidence repo; keep only if `artifacts/` is named as the public dataset in the same paragraph |
| `START-HERE.md` | `https://github.com/thisisntjon/poketcg` | leave-with-caveat | Click-through to a private repo; already says “not this repo,” but a judge still hits 404/private |
| `START-HERE.md` | `https://github.com/thisisntjon/thebus` | leave-with-caveat | Retired/private sibling; already marked RETIRED — keep the retraction sentence adjacent |
| `LAWS.md` | `~$49,686` API-list-equivalent (Law 9) | rewrite-in-place | Constitution quotes an unverified dollar; screenshot reads as proven spend. Drop the figure; keep the law. Do not invent a substitute dollar |
| `LAWS.md` | first-name `Jon` (Law 7 earned-by) | rewrite-in-place | First name + GitHub `thisisntjon` + `C:\Users\thisi` is a deanonymization chain |
| `scripts/spend_check.py` | `~$49,686` in module docstring | rewrite-in-place | Checker’s own comment banks the unverified Law-9 dollar as the incident. Keep the check; drop the number |
| `scripts/spend_check.py` | `Path.home() / ".claude" / "planning" / "refinery" / "data"` | rewrite-in-place | Default meter path is a personal Claude/refinery home layout |
| `workflow/PLAN.md` | `https://claude.ai/code/artifact/a82abedd-c7de-4407-9a4c-b9e5bfb1cf86` | rewrite-in-place | Session artifact URL; not a durable citation. A judge clicks it and gets login/404 |
| `workflow/PLAN.md` | same artifact URL (corpus audit primary) | rewrite-in-place | Second paste of the same non-public URL |
| `workflow/PLAN.md` | first-name `Jon` (×4: pending Jon / not Jon / Jon approved) | rewrite-in-place | Operator first name in the paused roadmap; screenshot = named principal |
| `workflow/blueprint/ARCHITECTURE.md` | `https://claude.ai/code/artifact/89126001-74c0-40a0-a00d-3ac69fe14a40` | rewrite-in-place | “Published view of the draft” is a Claude session link, not a paper |
| `workflow/blueprint/HARDENING.md` | `$120k` title: “Harden the recovered $120k” | rewrite-in-place | Headline dollar. **This is a replacement-cost memo, not cash or revenue.** A judge will still crop “recovered $120k” as valuation |
| `workflow/blueprint/HARDENING.md` | `$120k` cost-to-recreate sentence (`$30k`+`$70k`+`$20k`) | rewrite-in-place | Same memo, now itemized. Screenshot looks like a priced asset. Replacement-cost, not metered cash |
| `workflow/blueprint/HARDENING.md` | `$120k` “turn $120k from a memo into CI” | rewrite-in-place | Admits it is a memo, then treats `$120k` as real. Replacement-cost language a judge will still bank |
| `workflow/blueprint/HARDENING.md` | `$20k` expected avoided waste | rewrite-in-place | Replacement-cost slice of the `$120k` memo; looks like a savings claim |
| `workflow/blueprint/HARDENING.md` | `$30k` executable (H1) | rewrite-in-place | Replacement-cost slice of the `$120k` memo |
| `workflow/blueprint/HARDENING.md` | `$30k` install path (H2) | rewrite-in-place | Replacement-cost slice of the `$120k` memo |
| `workflow/blueprint/HARDENING.md` | `$70k` inspectability (H3) | rewrite-in-place | Replacement-cost slice of the `$120k` memo |
| `workflow/blueprint/HARDENING.md` | `$20k` option (H4) | rewrite-in-place | Replacement-cost slice of the `$120k` memo |
| `workflow/blueprint/HARDENING.md` | `$30k+$70k` portability (H5) | rewrite-in-place | Replacement-cost slice of the `$120k` memo |
| `workflow/blueprint/HARDENING.md` | `$20k` + C12 (H6) | rewrite-in-place | Replacement-cost slice of the `$120k` memo |
| `workflow/blueprint/HARDENING.md` | `$70k` C-family (H7) | rewrite-in-place | Replacement-cost slice of the `$120k` memo |
| `workflow/blueprint/HARDENING.md` | `$30k` continuity gap (H8) | rewrite-in-place | Replacement-cost slice of the `$120k` memo |
| `workflow/blueprint/HARDENING.md` | `C:\Users\thisi` (strip instruction) | rewrite-in-place | Documents the exact home path the factory still carries |
| `workflow/blueprint/HARDENING.md` | `C:\Users\thisi` (done-when grep) | rewrite-in-place | Same path token used as a success criterion |
| `workflow/blueprint/HARDENING.md` | `~/.claude/skills` | rewrite-in-place | Home-relative Claude skills path; second-machine leak |
| `workflow/blueprint/PLAN.md` | `~$120k` of recovered portable yield | rewrite-in-place | Problem statement prices the factory. **Replacement-cost memo, not earned cash** |
| `workflow/blueprint/PLAN.md` | “Hardening is how the $120k stays real” | rewrite-in-place | Treats the memo dollar as a thing that can “stay real.” Screenshot = valuation |
| `workflow/blueprint/PLAN.md` | “harden $120k now” | rewrite-in-place | Third `$120k` hit; same replacement-cost memo |
| `workflow/blueprint/PLAN.md` | `C:\Users\thisi` (H5 path-free row) | rewrite-in-place | Plan table still names the desktop username |
| `workflow/blueprint/PLAN.md` | first-name `Jon` (original hypothesis byline) | rewrite-in-place | Attributes the value-hardening prompt to Jon by name |
| `workflow/blueprint/EXTRACT-LOG.md` | `~/.claude/skills/…` (×9 rows) | rewrite-in-place | Extract log is a map of the author’s Claude skills directory |
| `workflow/blueprint/capabilities/09-method/README.md` | `~/.claude/skills/phased/` | rewrite-in-place | Capability README points at a home skills path |
| `workflow/canon/DECISIONS.md` | `~$49,686` (open verification item) | leave-with-caveat | This *is* the caveat that the Law-9 dollar is unverified. Keep only if LAWS/spend_check no longer cite it as earned-by fact |
| `workflow/canon/DECISIONS.md` | `~$49,686` (decision-table incident) | rewrite-in-place | Table presents the dollar as the incident that earned Law 9. Same unverified token; do not invent a replacement |
| `workflow/canon/DECISIONS.md` | “Private remote `thisisntjon/thefleet`” | rewrite-in-place | Settled decision still says the public-facing remote is private |
| `workflow/canon/DECISIONS.md` | first-name `Jon` (×5) | rewrite-in-place | Decision log is full of “Jon asked / Jon’s goal / Jon to confirm” |
| `workflow/experiments/2026-08-24-pr-case-study.md` | `C:\Users\thisi\Desktop\Pokemon` DEPLOYED_FORM | rewrite-in-place | Pre-reg pins the private mill to a home path; looks like hidden data |
| `workflow/handoffs/2026-08-08-p1-complete.md` | `https://claude.ai/code/artifact/a82abedd-c7de-4407-9a4c-b9e5bfb1cf86` | rewrite-in-place | Handoff cites a Claude artifact as “corpus audit source” |
| `workflow/handoffs/2026-08-31.md` | “private remote” for `thisisntjon/thefleet` | rewrite-in-place | Resume memo tells the next session the GitHub remote is private |
| `workflow/harvest/INVENTORY.json` | `C:/Users/thisi/Desktop/bonkers` | omit-from-public-view | Source list is a personal-desktop map (live protocol folder) |
| `workflow/harvest/INVENTORY.json` | `C:/Users/thisi/Desktop/Pokemon/playbook` | omit-from-public-view | Desktop path into the private mill playbook |
| `workflow/harvest/INVENTORY.json` | `C:/Users/thisi/Desktop/Pokemon/scripts` | omit-from-public-view | Desktop path into mill scripts |
| `workflow/harvest/INVENTORY.json` | `C:/Users/thisi/Desktop/Pokemon/ptcg-agent/harness` | omit-from-public-view | Names the harness mill on disk |
| `workflow/harvest/INVENTORY.json` | `C:/Users/thisi/.claude/skills` | omit-from-public-view | Absolute home + Claude skills |
| `workflow/harvest/INVENTORY.json` | `C:/Users/thisi/Desktop/Write-Up` | omit-from-public-view | Names a separate strategy workspace on the same desktop |
| `workflow/harvest/INVENTORY.json` | `Desktop/Write-Up` (H-098) | omit-from-public-view | Short-form desktop product path |
| `workflow/harvest/INVENTORY.json` | `Desktop/Career 2026` (H-099) | omit-from-public-view | Job-pipeline folder name + “93k json” on the author’s desktop |
| `workflow/harvest/INVENTORY.json` | `~/.claude/skills` rows (H-085–H-089, H-103) | omit-from-public-view | Harvest rows are a skill-directory inventory of one machine |
| `workflow/harvest/INVENTORY.md` | `~/.claude/skills` | omit-from-public-view | Prose twin of the JSON source map |
| `workflow/harvest/IDEAS.md` | first-name `Jon` (×4) | rewrite-in-place | “This is the harvest Jon asked for” — named principal |
| `workflow/harvest/IDEAS.md` | `false BO3/$50k` (I-K04) | rewrite-in-place | Invented prize-structure dollar; screenshot reads as a `$50k` prize |
| `workflow/harvest/PLAN.md` | first-name `Jon` (×5) | rewrite-in-place | Harvest plan bylines the operator |
| `workflow/harvest/PLAN.md` | “sale price of 10 files ≈ $0” | leave-with-caveat | Valuation language; keep only if clearly marked as a rejected lens |
| `workflow/measurements/2026-08-08-p2c-independent-cold-score-v3.json` | `C:/Users/thisi/Desktop/Pokemon/human-delta` | rewrite-in-place | Reproduce string is a home path into a private dest |
| `workflow/receipts/2026-08-08-law9-spend-lesson.md` | `$49.7k` lesson | rewrite-in-place | Rounded Law-9 dollar (same unverified incident as `49,686`). Do not invent a replacement |
| `workflow/receipts/2026-08-08-law9-spend-lesson.md` | first-name `Jon` | rewrite-in-place | “Jon reads the first real spend_check verdict” |
| `workflow/receipts/2026-08-31-factory-github.md` | “private GitHub” / “private remote” | rewrite-in-place | Banked receipt titled as a private-remote bind |
| `workflow/research/2026-08-24-pr-case-study/PAPER.md` | `C:\Users\thisi\Desktop\Pokemon` | rewrite-in-place | Methods pin the paper to a home clone; looks like unreproducible private data |
| `workflow/research/2026-08-24-pr-case-study/REPORT.md` | `C:\Users\thisi\Desktop\Pokemon` (`git fetch`) | rewrite-in-place | Reproduce block is three home-path commands |
| `workflow/research/2026-08-24-pr-case-study/REPORT.md` | `C:\Users\thisi\Desktop\Pokemon` (`rev-parse`) | rewrite-in-place | Same home path, second command |
| `workflow/research/2026-08-24-pr-case-study/REPORT.md` | `C:\Users\thisi\Desktop\Pokemon` (measure script) | rewrite-in-place | Same home path, third command |
| `workflow/research/2026-08-24-pr-case-study/REPORT.md` | “Prior Write-Up figures” | rewrite-in-place | Names another desktop product as the source of lore numbers |
| `workflow/research/2026-08-24-pr-case-study/join_mentions.py` | `Path(r"C:\Users\thisi\Desktop\Pokemon")` | rewrite-in-place | Hard-coded default clone path |
| `workflow/research/2026-08-24-pr-case-study/label_sample.py` | `Path(r"C:\Users\thisi\Desktop\Pokemon")` | rewrite-in-place | Hard-coded default clone path |
| `workflow/research/2026-08-24-pr-case-study/measure_pr_census.py` | `C:\Users\thisi\Desktop\Pokemon` default | rewrite-in-place | CLI default is the author’s desktop; a stranger running the script hits that path |
| `workflow/research/2026-09-01-public-display/PLAN.md` | “private measurement protocol” | rewrite-in-place | Investigation plan still frames the object as private |
| `workflow/research/2026-09-01-public-display/PLAN.md` | contest-readiness `47/100` (×2) | omit-from-public-view | Internal panel score; a judge will treat 47 as the official grade |
| `workflow/research/2026-09-01-public-display/PLAN.md` | Pokemon mill `~683` scripts / hub `4787` ahead | omit-from-public-view | Private-mill internals; screenshot looks like hidden scale |

## Class totals (how the 85 rows add)

| class | rows | grep basis |
|---|---|---|
| Desktop `C:\Users\thisi` (backslash) | 15 | G1 = 15; one row per line |
| Desktop `C:/Users/thisi` (forward) | 7 | G2 = 7; one row per line |
| Short desktop (`Desktop/Write-Up`, `Desktop/Career 2026`) | 2 | extra; not in G1/G2 |
| `claude.ai` / `claude.ai/code/artifact` | 6 | G5 = 6 (G4’s 5 plus T-002 class mention) |
| `$120k` / `120k` | 9 | G6 = 9; **every hit has a row** (T-002 L25, L37, L43) |
| `49,686` | 6 | G9 = 6; **every hit has a row** (T-002 L26 and L37 are separate rows) |
| README `(private)` leftovers | 2 | G11 = 2 |
| Other “private remote / private poketcg / private protocol” | 7 | T-004×2, DECISIONS, handoff + factory receipt, public-display PLAN, README poketcg cite (not the two README “private” leftovers) |
| HARDENING `$30k`/`$70k`/`$20k` slices (not already a `$120k` line) | 9 | replacement-cost language |
| `$49.7k` rounded Law-9 | 1 | related unverified dollar |
| first-name `Jon` (one row per file) | 7 | G12 = 21 hits / 7 files |
| `~/.claude` (file-level, not already a `C:/Users/thisi/.claude` row) | 5 | G13 = 18 |
| `spend_check` home meter path | 1 | other |
| contest `47/100` / mill `683`/`4787` / Write-Up lore / `$50k` / `$0` sale | 6 | other |
| START-HERE poketcg + thebus URLs | 2 | other |
| T-001 leftover-private + 47/100 (combined with its 47/100) | counted in T-001 third row | — |

Row arithmetic: 15+7+2+6+9+6+2+7+9+1+7+5+1+6+2 = **85**.
T-002 L37 is two physical rows (one per required token). T-001 leftover-private/`47/100` sits in the “other” 6, not in G1.

## Builder defaults (for T-006 / the later board)

1. **Public front door:** rewrite README private leftovers in-place when the public object ships. Visibility flip remains a human gate.
2. **Dollars:** HARDENING/PLAN `$120k` and `$30k`/`$70k`/`$20k` are replacement-cost memo language — rewrite to that phrase without a number, or omit the hardening memo from the public tree. `49,686` / `$49.7k`: drop the token; do not replace it with a new dollar; do not add it to `RETRACTIONS.md` unless it is shown false (token-match would fail `onboard_check` on DECISIONS if the caveat row stayed).
3. **Paths:** research scripts already accept a clone argument — delete the `C:\Users\thisi\Desktop\Pokemon` default. Harvest `INVENTORY.json` sources[] is a desktop map: omit-from-public-view or strip to logical names (`poketcg/playbook`, `user-skills`).
4. **Claude artifacts:** delete the three URLs; point at in-repo files only.
5. **Board tickets / investigation PLAN scores / mill head-counts:** omit-from-public-view.
6. **First-name Jon:** rewrite to “principal” / “the operator” wherever the public object keeps the file.

## Not landmines (checked, excluded)

- GitHub identity `thisisntjon` in `README.md`, `CITATION.cff`, `LICENSE`, `START-HERE.md` — intended public author string, not a desktop path.
- `thisisntjon` inside `workflow/research/2026-08-24-pr-case-study/artifacts/*.jsonl` — commit author field of the pinned census, not `C:\Users\thisi`.
- `poc@example.invalid` in `scripts/poc_check.py` — fixture email.
- Experiment receipts `~$0 API` — local CPU, not a valuation.
- `Fleet/`, `web/`, humanizer, `seed.md`, `valueproject.md` — not in `git ls-files`.
- HARDENING “Do not cite unverified Law-9 dollars” — hygiene prose, not a dollar hit.

## Out of scope (as ticketed)

No rewrites applied. `LAWS.md`, `README.md`, `LICENSE`, and `.github/workflows/verify.yml` were not edited.
)
