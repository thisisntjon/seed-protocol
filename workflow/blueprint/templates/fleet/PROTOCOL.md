# MAILBOX PROTOCOL

**Downstream (lead → agent):** `workflow/mailbox/INBOX-<name>.md` on origin/main.
Append-only, newest at top. **Only the lead writes these** — `main` push is lead-only, so
inbox authenticity is structural. Agents propose; the lead converts proposals into entries.

```
## [A-<name>-NNN] <UTC> - <one-line title>
STATUS: OPEN | SUPERSEDED | DONE(<utc>)
<full assignment text>
```

**Upstream (agent → lead):** branch `status/<name>`:
- `STATUS.json`: name, ts, assignment_id, state (WORKING|BLOCKED|IDLE|DONE), detail, eta,
  blocked_on, principal_needed, work counters (VALUE-delta, not ACTIVITY-delta).
- `reports/<utc>-<assignment-id>.md` pushed BEFORE taking new work.

**Rules (each earned — see harvest IDEAS F-family):**

- WAKE: own-inbox SHA diff + ≤30 min time baseline. Smoke-test new watchers.
- UNBLOCK-NOTIFY: blocker clears → inbox entry same cycle.
- LEAD-QUESTION: state=BLOCKED + blocked_on="lead: …" only.
- STALE-ORDER: consume entire inbox backlog; later entries supersede.
- CADENCE: chain every already-authorized step in one wake.
- DAEMON HEARTBEATS: shell-level; VALUE-delta proves work.
- WAITS ARE FIELDS: blocked_on="<target>: <what>"; bg: for parked secondary waits.
- TO: header is delivery; mid-body mentions are not.
