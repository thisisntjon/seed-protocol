# C02 — Orientation

Status: SHIPS

## User job

Any harness, any vendor, answers “what is true and what is next” in one command without
remembered state.

## Deliverable

```
python workflow/blueprint/bin/orient.py
```

Prints SHA, START-HERE four lines, current plan stage, open gates, newest handoff, next
action. Refuses if START-HERE is missing.

## Output location

`workflow/blueprint/bin/orient.py`

## Quality bar

`bin/selftest.py` sabotages a copy with no START-HERE and requires a non-zero exit.

## Remaining work

Budget-bounded token cap on printed bytes (ARCHITECTURE open item). First cut is short
by construction.

## Taken from

Playbook orient.py contract; AGENTS loop step ORIENT; harvest I-G01.
