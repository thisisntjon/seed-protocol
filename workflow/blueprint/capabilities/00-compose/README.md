# C00 — Compose

Status: DOCUMENTED

## User job

Turn a problem into inspectable work: request → plan → run → artifact → review, without
the session being the system of record.

## Deliverable

A project that has PLAN.md (phased), receipts for closed loops, and GATES for
irreversibles. Miracle's suite model applied to development.

## Output location

`workflow/PLAN.md`, `workflow/receipts/`, `GATES.md`, this catalog.

## Quality bar

- PLAN has Current stage + assumption registry.
- A DONE receipt has EVIDENCE a third party can re-run.
- Human gates have an SLA.

## Remaining work

Graph runner (Miracle-style DAG) is not needed for v1. Receipts + phases are the graph.

## Taken from

`miracle/docs/suite-workflow-architecture.md`, `playbook/README.md` eight ideas.
