# GRAPH — flywheels + handoffs

1. **Self-fueling flywheels.** Each compute box has a DEFAULT JOB when its queue is empty.
   "Idle awaiting another box" is not a legal state.
2. **Producer owns the bridge.** DONE = consumer's exact filename + sha, on the consumer's
   watched surface, plus a ledger row. A broker put is not delivery. A chat "ready" is not
   delivery.
3. **Handoff SLA** (default 15 min) on every declared producer→consumer edge, including the
   lead's merge queue.

Author XOR verifier stays cross-box: the box that built the artifact does not issue its
promotion verdict.

| edge | producer | consumer | artifact + marker | state |
|---|---|---|---|---|
