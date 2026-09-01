# GATES — the human-key boundary

Humans decide these and only these (Law 7). Edit the list for this project; do not copy another
project's irreversibles.

1. **Spend** above the pre-authorized runway (API budgets, purchases, subscriptions).
2. **Publication** — anything leaving the machine for an audience (posts, submissions, releases).
3. **Deletion / destruction** of non-regenerable data.
4. **Production flips** — deploys, submissions to live systems, credential changes.
5. **Scope changes** that invalidate the plan's problem statement.

Everything else: agents proceed and leave receipts. Asking permission for reversible,
in-scope work is a contract violation, not politeness.

## The SLA

**An OPEN gate older than 48 hours is an incident.** `scripts/onboard_check.py` fails the repo
until it is answered or explicitly deferred (status DEFERRED with a revisit date).

Answering a gate is always legal in any state; deferring it requires a date.

## Gate registry

<!-- GATE-REGISTRY machine-parsed by scripts/onboard_check.py
     status: OPEN | ANSWERED | DEFERRED(YYYY-MM-DD)
     SLA breach = status OPEN and opened > 48h ago -->

| id | what | decision needed from | opened | status |
|---|---|---|---|---|
