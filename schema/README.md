# schema/ — the evidence contract, machine form

**Incident that earned this directory (2026-09-02 external review):** a reviewer could not
inspect the evidence contract without reading the whole repository; the schemas existed only as
markdown templates. This directory is the answer: one JSON Schema (draft 2020-12) per record
type, plus a kernel that ties them together, so the contract can be read in one place and
validated by a machine.

## Two forms, one contract

| Form | Where | Audience |
|---|---|---|
| Human | `workflow/templates/RECEIPT.md`, `DISPATCH.md`, `EXPERIMENT.md`, `HANDOFF.md` | Whoever writes a record — copy, fill every field |
| Machine | `schema/receipt.schema.json`, `dispatch.schema.json`, `experiment.schema.json`, `handoff.schema.json`, and `evidence-kernel.schema.json` | Whoever validates or reviews the contract |

The templates remain authoritative for *what to write*; the schemas restate the same field
names, required fields, and closed vocabularies so a reviewer can check the contract without
reading the checker's source. Every field `description` is taken from the template text.

**The checker enforces both.** `scripts/onboard_check.py` validates the templates (they still
expose their fields) and every banked instance. `scripts/schema_check.py` parses every file in
`workflow/receipts`, `workflow/dispatches`, `workflow/experiments`, and `workflow/handoffs` with
the same field-extraction the checker uses and validates it against these schemas. It also
refuses to pass if the kernel's vocabularies drift from the checker's constants, so the two
cannot silently disagree. `scripts/sabotage_test.py` proves both fail on seeded defects.

```
python scripts/schema_check.py      # exit 0 = every banked record matches its schema
```

## Record types

| Directory | Schema | Record shape |
|---|---|---|
| `workflow/receipts/` | `receipt.schema.json` | `FIELD: value` lines; STATE and PROGRESS are closed vocabularies |
| `workflow/dispatches/` | `dispatch.schema.json` | `FIELD: value` lines; ACCEPTANCE and FENCES are required |
| `workflow/experiments/` | `experiment.schema.json` | `FIELD: value` lines; OUTCOME's first token is a closed vocabulary |
| `workflow/handoffs/` | `handoff.schema.json` | Headed document: first line `# RESUME HERE`, five required `## ` headings |

Closed vocabularies (restated in the kernel under `vocabularies`, identical to
`scripts/onboard_check.py`):

- `STATE`: DONE, PARTIAL, BLOCKED, KILLED, INVALIDATED
- `PROGRESS`: DECISION, MEASUREMENT, INFRASTRUCTURE
- `OUTCOME`: PENDING, PASS, KILL, NULL, INVALID-INSTRUMENT

## How the schema maps to the checker (read before tightening anything)

The schemas describe what the checker *already accepts* on 2026-09-02, nothing stricter. Where
the checker is looser than the template prose, the schema follows the checker, because tightening
would fail banked files, and banked files are not edited (Law 6: correct by ledger, not by rewrite).

- **Field extraction.** A field is any line matching `^[A-Z][A-Z0-9_]*:\s*(.*)$`; the value is
  the rest of that line, stripped. Continuation lines are not part of the value. Unknown fields
  are allowed (`additionalProperties: true`) — banked records carry `NEXT_EVENT`,
  `AMENDMENT_BEFORE_RUN`, `TERMINAL_NOTE`, etc.
- **Case.** The checker uppercases STATE, PROGRESS, and the first OUTCOME token before matching.
  `schema_check.py` applies the same normalization before validation; the enums are uppercase.
- **OUTCOME** is `<TOKEN>` optionally followed by whitespace and free text (measured value,
  receipt path), exactly as the checker splits on the first whitespace. `PASS (instrument). ...`
  is valid; `looks promising` is not.
- **Required receipt fields** are the checker's seven (STATE, OBJECT, EXACT_REF, EVIDENCE,
  PROGRESS, EFFECT, NEXT_OWNER), not the template's full list. `BLOCKED_ON` is required only
  when STATE is BLOCKED (encoded as `if/then`). `SESSION_ID` is required for receipts dated
  2026-08-09 or later; that cutoff depends on the *filename*, which is not part of the record,
  so the checker enforces it and the schema documents it.
- **Placeholders.** A required field that still contains `<...>` fails (the checker's
  placeholder rule), encoded as `not: {pattern: "<.*>"}` in the `filled` definition.
- **EFFECT honesty.** A DONE or KILLED receipt with PROGRESS DECISION or MEASUREMENT may not
  have an EFFECT starting with "none" (encoded as `if/then` + `not`).
- **EXACT_REF git existence** (a 7–40 hex ref must resolve to a commit) needs a git clone and is
  enforced by the checker only.
- **Handoffs.** The `## OPEN QUESTIONS` heading may carry a suffix (the template's own does);
  the checker matches headings as substrings, so the parser canonicalizes to the five prefixes.

Nothing had to be loosened below what the checker accepts: on 2026-09-02 all 33 pre-existing banked records
(22 receipts, 8 experiments, 3 handoffs, 0 dispatches) validate unchanged.

## Validator

`scripts/schema_check.py` has no third-party dependency. It implements only the keywords these
schemas use (`type`, `enum`, `const`, `pattern`, `minLength`, `not`, `properties`, `required`,
`additionalProperties`, `allOf`, `if`/`then`, `$ref` to `#/$defs` and to sibling files) and
raises on any other keyword, so a schema edit the validator cannot enforce is loud, not silent
(Law 2). Any conforming external JSON Schema validator should reach the same verdicts on the
same parsed records.

Version `0.1.0`. Bumping a schema requires a named incident and a DECISIONS row, like any
other addition to this skeleton.
