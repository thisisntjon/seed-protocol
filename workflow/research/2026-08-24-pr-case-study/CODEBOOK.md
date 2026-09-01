# Codebook — automatic labels

Instrument: `measure_pr_census.py` on first-parent history of pin SHA.

| Label | Rule |
|---|---|
| `docs_only` | Every changed path suffix is `.md` or `.txt` |
| `has_code` | At least one path suffix in `.py .go .js .ts .rs .java .c .cpp .h` |
| `other` | Neither (JSON, YAML, CSV, PNG, lockfiles, etc.) |
| `small` | `git numstat` additions + deletions < 100 (binary rows counted as 0 churn) |
| `title_class` | squash subject contains `[bank]` `[ops]` `[instrument]` `[research]` (case-insensitive) |

These are **file-shape** labels, not ground-truth “ceremony vs science.” A 2,000-line
markdown audit can be load-bearing; a 20-line Python tweak can be noise. The labels
answer: *what kind of bytes landed on main via a PR-shaped commit.*

## Pass-2 intent (n=80 sample only)

Exclusive. Defined in `pass2_labels.py`. PRODUCT = playing agent or ship payload.
INSTRUMENT = harness/eval/test/guard. EVIDENCE = measurement receipt. GOVERNANCE =
board/inbox/proposal/design/writeup. CEREMONY = cycle log / index / bus rotation.
OTHER = empty merge.

Pass 1 (`label_sample.py`) is keyword+path and over-calls EVIDENCE; pass 2 is the
reported distribution. One inspector. Exact agreement 50/80.
