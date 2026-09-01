# DECISIONS — settled. Do not re-litigate without new evidence.

**Caveat on the "rules as prose or checks?" rationale (added 2026-08-18).** The quoted sentence
is not a measurement. Its source, `poketcg/playbook/RULES-LEDGER.md`, has columns Rule / Origin
incident / Enforcement / Port — the origin incident is what *created* each rule, not what happened
after it existed, and the file contains no recurrence tracking. An external audit reports the claim
began as a 7-rule, 48-hour observation and was scaled to a header describing 73 rows. The DECISION
may still be correct — encoding rules is cheap and low-risk — but it currently rests on an untested
hypothesis, not evidence. The blueprint's enforcement layer is designed to measure it properly.
Not entered in RETRACTIONS.md because the claim is unverified rather than demonstrably false, and
because that file is token-matched: retracting the string would fail the checker on this row.

**Open verification item (2026-08-18).** `LAWS.md` Law 9 cites ~$49,686 as the incident that earned
it. Two independent audits of the source project report the figure does not appear there, and that
`playbook/COST.md`'s dollar cells are empty checkboxes. Unresolved; Jon to confirm the source before
the figure is cited again.

New sessions re-opening closed questions is a documented failure mode. A row here means the
question was decided with reasons; proposing the alternative again requires citing evidence that
did not exist at decision time. New decisions are recorded here in the same session they're made.

| decided | question | decision | why | reopen only if |
|---|---|---|---|---|
| 2026-08-31 | What is the GitHub identity, and what is the public-facing genre? | Private remote `thisisntjon/thefleet`. `README.md` is a research abstract (question, claim status, limitations, reproduce, cite). `START-HERE.md` remains the machine door. First push is factory extract + H1, not VoiceCraft or valuation memos. | Disk-only factory expires; a product landing page would overclaim C-004 | Public visibility flip (that is a GATES publication); or a named decision to merge VoiceCraft into this repo |
| 2026-08-23 | Merge Pokemon + Career + Bonkers into one factory repo? | No. Transplant CORE. Load OPTIONAL by extra. Keep domain packs in origin repos. Harvest lives at workflow/harvest/. | 646-tool sprawl is the anti-pattern; playbook TOOLS.md already says rebuild abstractly | A named incident shows CORE is insufficient for a second real project |
| 2026-08-23 | Is the harvest a file pack or an ideas factory? | Ideas factory. `IDEAS.md` is the growing ledger of development doctrine earned in production. The file pack encodes a subset. New incidents add rows, then checks. | Jon: inventory the ideas used DURING the project; a 10-file sale price is the wrong lens | A second real project shows a missing family that cannot be expressed as an idea+check |
| 2026-08-18 | Does the blueprint supersede SEED, or sit alongside it? | The blueprint supersedes SEED; SEED becomes an input, not a peer | Jon's goal is one reusable asset carried project to project, not two things to maintain that drift apart | Jon rescinds; or the blueprint fails to reach a working clone-and-go state |
| 2026-08-18 | When poketcg findings conflict with current state of the art, which wins? | SOTA wins by default; poketcg findings must earn their place against current evidence | A blueprint is where scar tissue calcifies into permanent workarounds for constraints that have since expired | A finding is operational knowledge that benchmarks structurally cannot measure |
| 2026-08-18 | Blueprint deliverable form | A clone-and-go repo template, working on day one with no setup ritual | A document still requires the work to be redone per project; the stated pain is that nothing was reusable | Never as a principle; the contents are open |
| 2026-08-08 | Default operating mode: fleet or single agent? | Single strong agent; fleet opt-in for provably independent tickets | 30-day fleet campaign produced zero confirmed improvements; multi-agent ~3× tokens, degrades interdependent work | An ablation (PLAN P3) shows the fleet winning on a real task |
| 2026-08-08 | Rules as prose or checks? | Every law that can be checked, is; PROSE laws are tracked debt | "Every encoded rule never failed again; every prose rule was violated at least once" — SEE CAVEAT BELOW: this rationale is UNVERIFIED | Never — this is the load-bearing bet of the skeleton |
| 2026-08-08 | Skeleton size | Small, incident-bounded core; additions require a named incident, but file count is not a target | 646-tool sprawl was the origin corpus's anti-pattern; the first working repository already exceeded the earlier approximate file count | Never as a principle; individual additions via incident |
| 2026-08-08 | Initial repository commit | Approved; establish the skeleton as a reproducible git object, then continue with bounded hardening | Jon asked Codex to use its review findings to continue the project after the uncommitted-state defect was identified | Only if Jon rescinds the continuation directive before the commit |
| 2026-08-09 | Add stress_test.py (incident: Jon requested large-scale local stress testing; prior evidence was 18 hand-picked sabotage cases) | Randomized defect-injection at scale, pre-registered bars (100% detection, 0 false alarms), deterministic seeds | Hand-picked cases prove existence of refutation power, not its coverage | The sabotage harness absorbs it, or a property-testing framework replaces both |
| 2026-08-08 | Add Law 9 + spend_check.py + FORECAST/SESSION_ID fields (incident: ~$49,686 API-list-equivalent metered against "zero confirmed improvements"; COST.md was empty checkboxes) | Spend is metered on a cadence; window spend above threshold with zero closed loops fails; dispatches forecast, receipts grade | The one thing the origin corpus exempted from its own evidence culture was its cost | A better metering substrate ships upstream |
| 2026-08-08 | Add status.py + checkpoint.py (incident: operator asked for progress visibility + checkpointing; origin incident: a daemon pulsed WORKING for 11h with zero output) | Progress derives from the PLAN table (no second state file); checkpoints are git commits gated on green checks | Progress that isn't tied to banked work is the lie the corpus already caught once | A better progress substrate ships in the harness itself |
