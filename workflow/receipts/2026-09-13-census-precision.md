STATE: DONE
OBJECT: Prepared the census precision correction for independent root review; no publication performed
EXACT_REF: working-tree-2026-09-13-census-precision-on-822fe1a1e1986edaed47db65296d95e69fbcbd5c
EVIDENCE: workflow/research/2026-08-24-pr-case-study/CORRECTIONS-2026-09-13.md records calculations and five pre-edit artifact SHA-256 values; 14 arithmetic/input checks passed; those five hashes are unchanged; all 14 raw-artifact/method files match baseline Git content. PAPER.md SHA-256 is 3a4149f8b3afe1740b1d93c16b2c2e1dcf5ebd9eb71c74ee49941258cc95c86c. Before this receipt, onboard passed with 0 errors/0 warnings, schema validated 32 records with 0 errors, and git diff --check passed. Required onboarding sabotage passed 23/23 and POC controls passed 22/22 before the edits; checker and method code are unchanged. Final onboard readback passed with 0 errors/0 warnings; final schema validation passed with 34 records and 0 errors, including this receipt and handoff; final git diff --check passed.
PROGRESS: DECISION
EFFECT: Current paper no longer treats file composition or the unweighted 2/80 sample as a measure or bound on useful output; numeric corrections include 17 bot-reviewed PRs with one overlapping author review, July 15's minimum code share, and sample code share 24/80 versus census 761/1,979
BLOCKED_ON: none for preparation; root owns independent review, commit and publication
SESSION_ID: Codex collaboration /root/site_delivery_review, 2026-09-13 census precision task
ACTUAL: One bounded editing pass; one preservation-check correction after a raw Git-blob comparison encountered the checkout's existing CRLF conversion. Git clean-filter identity and pre-edit byte hashes passed without changing protected files. No census rerun, relabelling, gameplay or new external model call
NEXT_OWNER: root, to review the working diff and publish only the reviewed correction
