# METRICS — health dashboard (pattern)

Rebuild rows from **this** project's surfaces. Do not import another project's numbers.

One family per failure class. Trends beat levels. Every alarm needs an owner.

## Flow (is work moving?)

| Metric | Healthy | Alarm |
|---|---|---|
| Verdict → next-job latency | inside your SLA | repeat breaches |
| Banked → shipped latency | hours | days (a proven artifact sitting is the ceremony pathology) |
| Handoff SLA breaches | 0/day | any repeat edge |
| Unclaimed ready work age | inside movement threshold | alarm |

## Liveness (is anything silently dead?)

| Metric | Healthy | Alarm |
|---|---|---|
| Heartbeat staleness while WORKING | < declared cadence | silence is an EVENT |
| VALUE-delta (not ACTIVITY-delta) | > 0 while WORKING | zero value > stall window |
| Unconfirmed dispatches | 0 at digest | any |

## Quality (is the evidence machinery working?)

| Metric | Healthy | Alarm |
|---|---|---|
| Verify coverage on promotion-feeding positives | 100% | any gap |
| Instrument sabotage coverage | 100% before first verdict | any unchecked instrument |
| Retraction rate | low, falling; nonzero is honesty | same mechanism twice |
| Prose-rule violations | falling | same rule twice → encode NOW |

## Economy

| Metric | Notes |
|---|---|
| Ceremony ratio (governance:construction) | pathology was ~3:1 |
| Wake efficiency | over-waking is a spend leak |
| Model-turns on courier work | should be ~0 (shell) |
| $/closed-loop | fill from principal spend + GATES count |

Coordination waste dwarfed token waste in the origin instance. Fix idle and ship-latency
before buying compute.
