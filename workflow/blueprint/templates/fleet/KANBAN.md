# KANBAN

Lead-owned. Cards carry: id, owner handle, **Files owned** (the mutex), Blocked-by,
acceptance criteria. Newest cycle state in an append-at-top header; older headers stay
below marked OLD.

**Claim = push a branch** `card/<id>-<handle>` before work starts. Branch existence is the
lock. Two live cards, same file = ERROR.

Support lanes when the queue is empty: RESEARCH / INVESTIGATE / PROPOSE / VERIFY. Never
idle, never invent scope.

## Ready

## In Progress

## Review

## Done
