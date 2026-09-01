# Factory ideas — what the campaign paid tuition for

**Stamped:** 2026-08-23
**Machine file:** `IDEAS.json`
**This is the harvest Jon asked for.** The file pack (`INVENTORY.md`, `pack/`) is how some of
these ideas are *already encoded*. This ledger is the asset: development ideas used during
the PTCG campaign (and the year of projects behind it), stripped of Pokémon, so the next
project does not re-derive them.

**Rule of this file:** it grows. A new project that hits an incident adds a row the same
cycle (idea → encode → check). It does not grow by importing 326 scripts.

---

## The forest

The expensive thing was not `status.py`. It was learning, in production, which ideas
actually hold:

- Git can be the whole coordination substrate.
- A session dying is normal; an org dying because state lived in a head is the failure.
- A green check that would stay green if the thing it describes were broken is worse than
  no check.
- A negative that overstates what it closed is more expensive than one that understates,
  because the overstatement is invisible.
- Local eval is a filter. Labels lie. Frozen legs look converged. Pair-means beat
  winner's-curse. Underpowered nulls are UNKNOWN, not refuted.
- The human should only press buttons that cannot be un-pressed — and a gate waiting on
  that human is the #1 project killer, so gates carry an SLA.
- Construction should be free; rigor lives at promotion.
- Idle is illegal; the producer owns the bridge; waits are fields; silence is an event.
- Domain expertise is not the prerequisite. Process judgment is. The human never needed
  to learn the game.

The playbook's own conversion rate: **nine days to discover this shape in production;
about one day of structure and three days of culture to stand it up elsewhere**
(`playbook/BOOTSTRAP.md`). The instance that discovered it was a 30-day fleet on top of a
year of projects. That tuition is the cost basis of this ledger. The mill (eval scripts,
wake `.ps1` files, kernel copies) is the *waste product* of discovering these ideas.
Keep the ideas. Do not import the mill.

**Causal savings versus a bare repo are still unmeasured** (Bonkers C-004, P3 ablation
pending). That does not make the ideas cheap. It means we have not yet priced the *payout*.
The *premium already paid* is the research.

---

## How a new project uses this

1. Solo default: families **A, B, C, D, E, J**. Encode as you hit them. CORE already
   encodes a subset (see `INVENTORY.md`).
2. Second agent or second box: families **F, G**.
3. Shipping to a real runtime: family **C** (deployed-form, identity-by-hash, preflight
   rebuilt for *that* runtime).
4. After every incident: add a row here, then a check. Never a new prose paragraph
   (rule diet).
5. After every surprise positive: suspect leakage, self-similarity, and "the ship path
   never carried the logic" before celebrating.

---

## A. Substrate — the repo is the memory

| ID | Idea | Earned by | Encode |
|---|---|---|---|
| I-A01 | **Git is the only control plane.** Claim by push, dispatch by inbox-on-main, report on status branches. Authenticity, locking, audit, crash recovery come free. | Clipboard courier; inbox forgery; hub checkout hijack | Doctrine; mailbox when 2nd agent |
| I-A02 | **The repo is the memory.** Sessions die constantly. State in artifacts, not context windows. Successor re-orients in minutes. | Three lead-session deaths in three days | CORE: templates + START-HERE |
| I-A03 | **START-HERE contains no sentence a later sentence corrects.** Historical contradiction lives in provenance files. Checker wins. | 66 files still citing a retracted figure; AGENTS.md as 500-line supersede stack | CORE: onboard_check paths + retractions |
| I-A04 | **Correct by editing; retract by ledger.** Grep finds the wrong answer first if you append-only-correct. | Same | CORE: RETRACTIONS token scan |
| I-A05 | **Never delete documentation.** Archive banner + supersession register. Missing files look like "n=0 / never done." | Fleet re-deriving from vanished citations | CANDIDATE (conflict: Bonkers overwrites *current* truth; archive research) |
| I-A06 | **Wake pack, not the novel.** Inventories + NOW + CURRENT-TRUTH. Do not open 600 research files on wake. | Harness accessibility; 44% of PRs were markdown-only | CANDIDATE: inventory_validate pattern |
| I-A07 | **Governance is origin/main, not the hub working copy.** | Local RUN_GATES 33 sequences stale | Doctrine |
| I-A08 | **No shallow git in the hub.** Shallow fetch destroyed merge-base, stranded 15h of read-side. | 2026-07-29 hub incident | Doctrine |
| I-A09 | **Dates cite their source artifact or are void.** Derived ceilings are not walls. | DATES.md D4 wrongly propagated as a schedule | Doctrine |
| I-A10 | **Handoffs shrink over time.** That trend is the health metric. | Lead handoff memos | CORE: HANDOFF.md |
| I-A11 | **Path-exists inventories beat hand maps for existence; a CURRENT file beats inventories for meaning.** | HARNESS_MAP product story went stale while paths were fine | CANDIDATE |
| I-A12 | **Forward slashes in every manifest on every OS.** | Third backslash incident | Doctrine |

## B. Evidence and promotion

| ID | Idea | Earned by | Encode |
|---|---|---|---|
| I-B01 | **Freeze the bar before the run.** Gate = pre-result commit on the shared remote. Self-asserted timestamps are unverifiable. | 7-second cross-machine timestamp | CANDIDATE: gate_pin |
| I-B02 | **One failed frozen criterion banks the negative.** No repair cycle, no post-hoc threshold. Amendments only pre-result. | "#819 pending full matrix" already failed ≥6 criteria | CORE: EXPERIMENT.md outcomes |
| I-B03 | **Exactly one machine-readable verdict token.** Hedge prose is not a verdict. | Same incident | CANDIDATE: verdict_lint |
| I-B04 | **Author XOR verifier.** Positives and first-use instruments need non-author reproduction. Negatives bank author-only same-cycle. Extended even to *hardware*: the box that built it never issues its verdict. | E016, #44, #48 in one day | CORE: AGENTS roles |
| I-B05 | **Sabotage before trust.** A guard is decorative until it fails the defect it claims to catch. Fresh fixtures, never the author's tests. | `0*64` hash gate; screen harness testing the wrong agent; PREFLIGHT PASSED with 14/23 skipped | CORE: sabotage_test |
| I-B06 | **Identity by hash, never label.** | "parity-v3" label pinned to generic-arm bytes | CORE: Law 3; transplant provenance |
| I-B07 | **Measure the deployed artifact, not the repo.** | Kaggle bundle silently played skip-bot while local evals looked fine (E016/E022); 133 deck files → 26 lists | CORE: Law 3; rebuild preflight per runtime |
| I-B08 | **CI-green ≠ gate-green ≠ admitted.** Compare number *and shape* to the frozen row before "pending/trending." | C-R0 pending-matrix hedge | Doctrine |
| I-B09 | **A number in a report is backed by an artifact committed in the same change.** Disk, worktree, and bus comments are not evidence. | Contaminated PRs that passed clean-diff | Doctrine |
| I-B10 | **No arm is spoken about before its matched control exists.** An n=20 look is not a result. | "940 kernel wins at 85%" reversed at n=300 | Doctrine |
| I-B11 | **Equation-bearing claims get arithmetic recompute** (units, denominators, freeze/maturity, one parameter model, ref/archive/sha joins). Clean diff cannot catch a cross-family join. | Four contaminated PRs in a day | CANDIDATE: SEMANTIC_EQUATION_VERIFY pattern |
| I-B12 | **Register discipline: append corrections; never rewrite banked history.** Original claim + error mechanism stay visible. | Actor/name errors vs source table | Doctrine |
| I-B13 | **Default disposition: NOT promotion-eligible** until author + independent verify + scope + power. | GATES template | CANDIDATE |
| I-B14 | **Reads are advisory the moment data exists; only SPENDS wait for confirmation.** | SD-13.2 | Doctrine |
| I-B15 | **A HOLD whose premise is withdrawn does not bind.** Silence is not a veto. | #1980 after superseding ruling | Doctrine |
| I-B16 | **Per-seat LATEST verdict at the exact head governs.** Older PASSes on moved heads are void. | Mid-review head moves | CANDIDATE: merge_head_guard |
| I-B17 | **Merging command re-reads full verdict set + head in one command.** Sample-then-merge is a defect. | #1980 trio complete while merge prose claimed HOLD | Doctrine |
| I-B18 | **Bank a binding change BEFORE the verifier polls.** | #1981 third bounce | Doctrine |
| I-B19 | **Delivery is claimed only after reading the artifact back from the consumer's surface.** A write landing is not delivery. | Fleet deafness / write-without-wake | I-F05 producer-owns-bridge |
| I-B20 | **Every byte a verifier reads is identity-bound** (bound path + sha before parse). | Journal/path forgery class #1980 | Doctrine |
| I-B21 | **Suspect leakage FIRST on any surprise positive.** | Cross-fold leakage turned +3.3pp into +0.50pp | Doctrine |
| I-B22 | **Transcribe, don't paraphrase, when folding findings into pre-regs.** | Round-3 integrity flag | Doctrine |
| I-B23 | **Pre-register families/sweeps, not single configs, when iteration is expected.** | 3-round refusal ping-pong | CORE: EXPERIMENT.md |
| I-B24 | **PREREG-CHECKLIST from YOUR refusals**, numbered, self-attested. Do not copy another project's refusal list. | Rep-3 negotiation | CANDIDATE |

## C. Measurement (eval as a discipline, not a Pokémon script)

| ID | Idea | Earned by | Encode |
|---|---|---|---|
| I-C01 | **Local eval is a filter, not a predictor** until a live calibration exists. | Ladder *inverted* local eval (v1.1 below random) | Doctrine; rebuild calibration per domain |
| I-C02 | **Power the instrument for the effect you care about.** Underpowered "null" is UNKNOWN, not refuted. +5–8pp claims need N that actually has power (here: ≥1200/arm; N=400 ~40% power at +6pp). | MDE 9.84pp at n=400 vs protocol needing 5–8pp | Doctrine; plug in *your* SE |
| I-C03 | **Cite the powered study, not the smoke.** n=20 "20-0" was labeled directional in its own source; the load-bearing result was N=100. | Search autopsy; 940-at-85% retraction | Doctrine |
| I-C04 | **Reachable ≠ selected ≠ executed.** Search body unreachable; policy branch never taken; 12/16 switches OFF in the shipped bundle. Ask which agent and demand the sha. | Two agents, fielded ≠ built | Doctrine |
| I-C05 | **Age-in-hours does not catch a frozen arm.** Need froze_at + matured. Pull poll history, never just the value. | 815.1 frozen pre-maturity quoted as best | Doctrine |
| I-C06 | **Pair-mean, not winner's curse.** Quoting the better copy of two is forbidden. | Protected floor 753.1 dropped the 711.2 draw | Doctrine |
| I-C07 | **Do not quote a point bar when the estimate is n=2–3.** Publish an interval. | 729.10 published as point four times | Doctrine |
| I-C08 | **A path you cannot read is not a path that is empty.** Name the box. | False "n=0, closed" from the other machine | Doctrine |
| I-C09 | **Self-similarity is not an opponent.** Scoring 97–99% against your own heuristic piloting their decks is not a field result. | Band-pool reclassification 2026-07-31 | Doctrine |
| I-C10 | **The ship path must carry the logic.** A knob experiment on a module the loader never imports is measuring a ghost. Config/env/flag that the deployed object cannot see does not exist. | rules_lucario knobs vs fielded single file; lazy imports stripped post-init | Law 3; capability manifest |
| I-C11 | **Vacuous counters.** An eager-default seam that bumps on every call is not evidence the candidate ran. Require verify() AND a nonzero *candidate* hook-resolution counter. | Three studies died; generic counter | Doctrine |
| I-C12 | **Skipped checks are not a pass.** Print how many checks actually ran. | PREFLIGHT PASSED 14/23 skip | Law 2 |
| I-C13 | **If the environment exposes no seed, seed-paired eval is impossible.** Don't pretend pairing. Throughput is the variance lever. | battle_start(deck0,deck1) only | Doctrine per ABI |
| I-C14 | **A flat pooled score can hide the band that matters.** FarmScore vs EliteFloor; harmonic mean so one easy band cannot hide a transition weakness. | Leaders farm the field and survive peers | CANDIDATE per domain |
| I-C15 | **Latency claims only from the mode that can support them.** Parallel runner outputs are WR-only. | pin2 vs workers | Doctrine |
| I-C16 | **Config overrides go through one API, then assert they landed.** Direct mutation of a module that can load twice is a silent no-op. | #96: 2,400 games on the default while claiming otherwise | Doctrine |
| I-C17 | **Dead-end rows carry a SCOPE GUARD:** what the evidence supports AND what it does not. Overstating a negative is the more expensive failure because it is invisible. | DEAD-ENDS.md purpose statement; A6 VOID almost closed the live lane | CANDIDATE |
| I-C18 | **Arithmetic can close a door independently of cell count.** Teacher μ below the wall means perfect imitation still loses; six failed cells were corroboration, not the ruling. | PLAN-LEARNING-LOOP criterion 8 / A13 | Doctrine |
| I-C19 | **Agreement-with-champion is ceilinged at reproducing the champion.** It can never demonstrate improvement *on* it. | SK-332/354 value-net | Doctrine |
| I-C20 | **"It imported" is not "it ran."** Symbols present, engagement vacuous, then 24-0 to its own fallback. | V13 search seq-89/90 | Doctrine |
| I-C21 | **Artifact identity chain:** code hash, data hash, config, experiment id, in every result file. | K-EVAL-25 provenance stamp | CANDIDATE |

## D. Method when the domain is unknown

| ID | Idea | Earned by | Encode |
|---|---|---|---|
| I-D01 | **Phased investigation:** frame → investigate → assumption registry → roadmap → phase loop. PLAN.md is state. Gates are approve/adjust, not approve/reject. | `/phased`; Bonkers PLAN | CANDIDATE skill; Bonkers PLAN format |
| I-D02 | **Existence-check before building.** Research whether the thing exists. | Jon operating contract | Doctrine |
| I-D03 | **Incident → rule → machine check, within one cycle.** | Playbook empirical claim (encode-recurrence still unverified as a *statistic*; encoding remains the cheap default) | CORE: Law 1 + meta-law |
| I-D04 | **Rule diet.** Incidents add a check or a checklist line, never a new prose rule. Prose gets compiled and retired. | Ceremony pathology: lots of experiments/cards/tools → few submissions | CORE: Law 1 |
| I-D05 | **Additions require a named incident.** No speculative structure. 646-tool sprawl is the anti-pattern. | Skeleton-size decision | CORE: LAWS meta-law |
| I-D06 | **Pivot-check when a load-bearing assumption flips.** Do not absorb silently. | `/phased` pivot-check | Doctrine |
| I-D07 | **Official scoring is the rubric.** Do not invent a 14/14/14 split or a Second-Round/BO3 prize. | ARCHIVE-CORRECTIONS; Strategy evaluation | Doctrine |
| I-D08 | **One north-star, then an answer map** (claims as a graph: requires / tests / supports / refutes / unlocks). Optional; not default factory. | 2026-08-23 answer-map work | CANDIDATE docs-only |
| I-D09 | **Control vs treatment identity.** Public baseline is a control, not the mission win. Ask which object. | OWNED-CORE vs public c61; two agents | Doctrine |
| I-D10 | **Process judgment, not domain expertise, is the human's job.** Persistence, irreversibles, priority. The team learns the domain from sources and measurement. | HOW-WE-GOT-HERE | Doctrine |
| I-D11 | **Genuinely different perspectives are load-bearing.** Adversarial second opinions; different model families that disagree usefully. | Playbook transferable claim 3 | Doctrine |
| I-D12 | **The learning loop is the product.** Week two runs on autopilot where week one ran on paste *because of the ledger*. | Playbook transferable claim 4 | This file |
| I-D13 | **It is teachable because it is written down.** Join, roster, idle behavior, orders, what counts as true, why each rule exists — an afternoon. | Playbook transferable claim 5 | START-HERE |
| I-D14 | **SOTA wins by default against calcified scar tissue.** A finding must earn its place against current evidence. | Bonkers DECISIONS 2026-08-18 | Doctrine |
| I-D15 | **Minimum viable subset:** solo operator + two agents yields the headline properties at roughly a fifth of the tooling. Default one strong agent; fleet is opt-in. | Playbook + Bonkers DECISIONS | CORE: Law 8 |

## E. Autonomy and the human

| ID | Idea | Earned by | Encode |
|---|---|---|---|
| I-E01 | **Humans gate irreversibles only** (spend, publication, deletion, production, scope). Everything else: proceed, leave receipts. Asking permission for reversible in-scope work is a contract violation. | TheHolyGrail died at "register the GitHub App"; The Village GATE PENDING a month | CORE: GATES.md + Law 7 |
| I-E02 | **An OPEN gate older than its SLA is an incident.** Waiting on the human is the #1 documented project killer. | Same | CORE: onboard_check SLA |
| I-E03 | **STOP table is tiny; everything else is LOG-AND-CONTINUE.** "If clearance doesn't check it, it cannot block." | Rule-diet finding | CANDIDATE: AUTONOMY template |
| I-E04 | **Staging ladder: autonomy proportional to reversibility.** Zero-key scratch → one-key candidacy → two-key promotion → Principal-key ship. | Playbook §4 | CANDIDATE |
| I-E05 | **Error budgets loosen when healthy.** Governance is not a one-way ratchet. | Ceremony pathology | Doctrine |
| I-E06 | **Rigor lives at promotion boundaries; construction runs free.** | Proven +15.2pp artifact sat 5–6 days unshipped; 4 zero-submission days | Doctrine |
| I-E07 | **Two-strike parks the LANE, never the box.** Fall through to the next runway item. | Fleet-wide idle over one blocked lane | Doctrine |
| I-E08 | **"Awaiting adjudication" is not a legal idle** while a pre-authorized runway exists. | Overnight rule | Doctrine |
| I-E09 | **The Principal is never the courier.** One aggregated 🔔 block per cycle. | Action items buried across terminals | Doctrine |
| I-E10 | **Escalation tiers.** SEV0 pages the human; SEV1 lead; SEV2 batched advisor. Nothing else pages. | Principal-channel noise | CANDIDATE |
| I-E11 | **Ask the team where it hurts** before buying compute or adding process. | Jul-16 interviews: coordination, not compute, was the constraint | Doctrine |
| I-E12 | **Worker dissent has standing.** Less-privileged alternative can win. | Roach objected to SSH elevation; watchdog without new privileges won | Doctrine |

## F. Fleet (opt-in — second agent / second box)

| ID | Idea | Earned by | Encode |
|---|---|---|---|
| I-F01 | **Claim-by-push; branch existence is the lock.** Alphabetically-first wins ties; post-work collisions ruled by pushed evidence. | Day-one collisions | When 2nd writer |
| I-F02 | **Files owned is the mutex.** Two live cards, same file = ERROR. | File-ownership collisions | CANDIDATE: board linter |
| I-F03 | **One persistent worktree per handle.** New card = branch switch, not a new folder. Never checkout the hub. | Hub hijack 2026-07-09; dirty-source copies | CANDIDATE: new_harness |
| I-F04 | **Idle is illegal. Flywheel = default job that never waits on another box.** | GRAPH.md | CANDIDATE |
| I-F05 | **Producer owns the bridge.** DONE = consumer's exact filename, sha-verified, on the watched surface, + ledger row. Broker put is not delivery. | Both directions of a cross-box transfer stalled | CANDIDATE |
| I-F06 | **15-minute handoff SLA** on every declared edge, including the lead's merge queue. | Stall forensics: lead review + one unowned handoff were the only bottlenecks | CANDIDATE |
| I-F07 | **Dual-trigger wake:** own-inbox SHA diff + ≤30 min time baseline. Events for speed, time for worst case; each covers the other's death. Firing on every main push is a spend leak. | Misty over-wake; time-only loop hour-scale latency + two false dead-watchers | Policy; do not copy .ps1 |
| I-F08 | **Waits are fields, not prose.** `blocked_on="<target>: <what>"`. `bg:` for parked secondary waits. | 45-min wait on an already-merged PR, invisible to every detector | CANDIDATE |
| I-F09 | **Stale-order rule:** on any wake, consume the ENTIRE inbox backlog. Later entries supersede. | Agent ran a superseded screen for hours | Doctrine |
| I-F10 | **Unblock-notify:** when a blocker clears, write the waiting agent an inbox entry the same cycle. | Ash and Brock sat silent on cleared blockers | Doctrine |
| I-F11 | **Cadence:** event-driven; chain every already-authorized step in one wake. Fixed intervals are fallbacks only. | "5080 metronome" sleeping between authorized steps | Doctrine |
| I-F12 | **VALUE-delta, not ACTIVITY-delta.** WORKING + zero value progress >2h = STALLED. Freshness of a PID is not health. | Harvest 0 eps for 11h as WORKING; dry harvest's activity counter defeated the flag | CORE: Law 8 spirit; encode in heartbeats |
| I-F13 | **Silence is an event.** Stale WORKING heartbeat is not "fine." | Lead-monitor design | Doctrine |
| I-F14 | **Remove the router from the loop.** Repeating routing pattern → standing order. Standing re-verify, class-token self-engage, movement audit. Agents cheap/parallel; lead attention serial. | 2026-07-18 movement wave; three finished items queued on routing | CANDIDATE |
| I-F15 | **TO:-header delivery.** Mid-body mentions are not delivery. | ACTIVE-COMMS / seq-132 | Doctrine |
| I-F16 | **Attribution is seat:field, not GitHub identity.** Same identity posts for every harness. | 07-29 verifier wrongly suspended | Doctrine |
| I-F17 | **Liveness is three-state:** advancing output, answered nonce, or lawfully-quiet (do not escalate as dead). | Jon-direct-busy stand-down | Doctrine |
| I-F18 | **O(1) backlog:** assign the top unassigned item only to an idle seat with empty queue. | BACKLOG.md | Doctrine |
| I-F19 | **main is lead-write-only.** Inbox authenticity is structural. | Agent wrote another's inbox claiming Jon approved | When 2nd agent |
| I-F20 | **Identity fixed, function fluid.** Names never change; functions re-sort around competence; org formalizes the re-sort. | "Leader" nickname drifted into implementation | Doctrine |
| I-F21 | **Repair worktrees BEFORE prune; KEEP ambiguous.** | Stray prune deregistered 22 worktrees | CANDIDATE: wt_sweep |
| I-F22 | **Watchers live OUTSIDE git worktrees.** Branch checkouts clobber in-tree watchers. | Windows-update deaths | FLEET |
| I-F23 | **Dual-channel box liveness** (git + beacon). Git-silent+beacon-alive = CHANNEL_ISSUE, not BOX_OFFLINE. | Remote git silence ≠ box death | FLEET |
| I-F24 | **Support lanes when the queue is empty** (research / investigate / propose / verify). Never idle, never invent scope. | Universal harness prompt | Doctrine |
| I-F25 | **Commit author is the handle**, per-command, never via shared git config. | Unattributable-commit incident | Doctrine |

## G. Continuity (session death is the default)

| ID | Idea | Earned by | Encode |
|---|---|---|---|
| I-G01 | **Orient before acting.** Never on remembered state. | Session blocked on a blocker resolved 12h earlier | CANDIDATE: orient.py |
| I-G02 | **OS scheduler, not a model session,** for digest and courier. Overnight work cannot depend on a chat being open. | Session-death blindness | CANDIDATE: ops_digest, queue_worker |
| I-G03 | **Dispatch ledger** recovers orders lost to crashes. | Windows update killed a dispatch in flight | CANDIDATE |
| I-G04 | **Deadlines file survives lead-session death.** New session re-arms from the file. | BOOTSTRAP | CANDIDATE |
| I-G05 | **LEAD-STATE pane** a successor lead resumes from. Do not trust older memos. | Successor-lead recovery cost | CANDIDATE |
| I-G06 | **Queue worker: fail-closed admission, caps, PARK on failure.** Authorization is declared state, not a cryptographic signature. Irreversible-shaped argv refused. | Runaway 35–42 GiB/h writers; force-bypass smuggling | CANDIDATE |
| I-G07 | **Long jobs: observable heartbeat AND incremental atomic checkpoint.** When blind to progress, check the checkpoint — don't kill. | Finished 9,726-row run nearly killed blind | Doctrine |

## H. Cost and throughput

| ID | Idea | Earned by | Encode |
|---|---|---|---|
| I-H01 | **Spend buys closed loops, and it is always metered.** Stale meter is a failure. Dollar figures from tokens are API-list-equivalent, never cash. | Evidence culture that exempted its own cost; COST.md empty checkboxes. *The specific dollar figure in Law 9 is unverified — keep the idea, not the number.* | OPTIONAL: spend_check |
| I-H02 | **Throughput is not progress.** Commits, PRs, tools, documents are activity. Progress = hypothesis → pre-registered test → verified result → decision. | 2,199 PRs with zero closed experiment loops for 24 days; 30-day fleet, zero confirmed improvements | CORE: Law 8, status.py |
| I-H03 | **Ceremony ratio** (governance:construction) as a dashboard number. | ~3:1 during pathology | METRICS pattern |
| I-H04 | **Wake efficiency.** Over-waking is a direct spend leak. | Misty watcher | I-F07 |
| I-H05 | **Model turns on courier/heartbeat work that a shell could do → ~0.** | Daemon-heartbeat rule | Doctrine |
| I-H06 | **Tier-match mechanical lanes.** Verifier reproductions of mechanical claims do not need frontier models. | COST.md lever 5 | Doctrine |
| I-H07 | **GPU duty cycle while everyone reports busy** is a diagnostic. | 10–20% measured | METRICS |
| I-H08 | **Banked→shipped latency** is the number that caught the 5–6 day stall of a proven artifact. | Stall forensics | METRICS |
| I-H09 | **Forecast every dispatch; grade actual on the receipt.** Calibration flywheel. | Law 9 FORECAST/ACTUAL | CORE: DISPATCH + RECEIPT |

## J. Tooling quality (any script, not the mill)

| ID | Idea | Earned by | Encode |
|---|---|---|---|
| I-J01 | **stdlib-only where the artifact ships.** Reviewable, no hidden deps. | Bundle constraints | Doctrine per runtime |
| I-J02 | **Exit codes are the API.** Everything gates on everything else. | TOOLS.md pattern | CORE checkers |
| I-J03 | **Fail closed, loudly.** Cannot measure ⇒ failure, never silence. "SKIPPED — not reporting clean." | status.py git-unavailable | CORE |
| I-J04 | **Each check cites its incident in-source.** Tools are the fossil record. | TOOLS.md | Doctrine |
| I-J05 | **Ambiguity resolves to KEEP or PARK, never proceed.** | wt_sweep; queue_worker | Doctrine |
| I-J06 | **QoL baseline for unattended jobs:** dry-run, idempotency, checkpoints, resume, timeouts, structured logs, cancellation, machine-readable output. Scale to project size; N/A is a valid verdict. | qol-baseline skill (22 items) | CANDIDATE checklist |
| I-J07 | **Non-destructive install.** Transplant refuses differing targets; identity files are never overwritten. | P2 transplant work | CORE: transplant.py |
| I-J08 | **Capability / switch manifest** for any product with dormant paths. Which switches are ON in the *shipped* object. | 12/16 switches OFF | CANDIDATE |

## K. Anti-patterns (negative ideas — also assets)

| ID | Idea | Do not |
|---|---|---|
| I-K01 | **The mill.** Hundreds of domain scripts are the waste product of discovery, not the factory. | Copy `ptcg-agent/harness/*` |
| I-K02 | **thebus.** A separate fleet-governance product, retired. Design retracted. | Rebuild a bus repo |
| I-K03 | **Mega-merge.** Pokemon + Career + Bonkers as one repo. | Union the trees |
| I-K04 | **Invented rubrics / prize structures.** | 14/14/14 splits; false BO3/$50k |
| I-K05 | **Provenance novels as current truth.** AGENTS.md 500-line supersede stacks. | Onboard from the novel |
| I-K06 | **Second state file** that drifts from PLAN. | A STATUS.md that is not derived |
| I-K07 | **Bulk `--apply` on a header-driven board.** | board_sync --apply |
| I-K08 | **Copying another project's live CLAIMS/PLAN/retractions.** | Identity overwrite |
| I-K09 | **Humanizer / product UI as protocol.** | Bonkers web/ + VoiceCraft in CORE |
| I-K10 | **Watcher scripts inside worktrees.** | I-F22 |
| I-K11 | **Treating a frozen or never-polled number as a score.** | I-C05 |
| I-K12 | **Closing a mechanism class because one implementation failed.** Scope guard or don't cite. | DEAD-ENDS A1/A2 |

---

## What is already encoded in CORE

Laws, onboard_check, sabotage_test, status-from-PLAN, checkpoint, transplant, dispatch /
receipt / handoff / experiment templates. That is the *minimum executable subset* of A–E
and H02/H09/J02/J03/J07.

Everything else in this ledger is **doctrine until the next project hits the incident**,
then it becomes a check. That is how the factory grows without becoming the mill.

## Value, said plainly

| Lens | What it is |
|---|---|
| **Tuition already paid** | Year of projects + a 30-day multi-agent production campaign + the research corpus. Principal's characterization: thousands of human hours. Playbook conversion: 9 days to discover, ~1+3 days to stand up if you follow the extract. |
| **What you would re-pay without this ledger** | Re-discovering I-C04 through I-C12 *in the next domain* (wrong object, vacuous counters, skipped preflight, frozen scores, self-similar opponents, ship path not carrying the logic). Those mistakes are not Pokémon-specific. |
| **Sale price of the git files** | Near zero. The files are small. |
| **Replacement cost of the ideas** | The campaign. That is the only honest cost basis. |
| **Payout** | Unmeasured until a second real project runs P3-style ablation (C-004). The factory exists so that measurement is possible *without* re-deriving the instrument. |

Do not capitalize campaign spend onto `onboard_check.py`. Capitalize it onto **this list**.
The growing factory is: hit incident → add row here → encode a check → never pay that
tuition again.
