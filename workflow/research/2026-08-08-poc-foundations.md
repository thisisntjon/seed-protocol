# POC foundations — measuring autonomy without measuring theater

Date: 2026-08-08  
Scope: just-in-time research for Bonkers P2/P3 instrumentation and The Human Delta pilot.

## Question

What must the first proofs of concept establish before this project can credibly become a
"thermometer" for the remaining human contribution in agentic work?

## Primary-source findings

1. **Use real tasks and human baselines.** OpenAI's MLE-bench uses 75 Kaggle competitions and
   derives human baselines from public leaderboards. Its resource-scaling and contamination
   analyses make clear that a score without a task distribution, budget, and exposure model is
   not an autonomy measurement.
   Source: https://openai.com/index/mle-bench/

2. **Difficulty belongs in human units.** METR measures task difficulty by the time an
   appropriately skilled human needs, then estimates an agent success curve over that duration.
   This gives the result an interpretable real-world unit and exposes the reliability collapse on
   longer tasks.
   Source: https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/

3. **Count the whole bill.** METR's expenditure-horizon work explicitly includes model tokens,
   experiment compute, and human labor, and argues for continuous cost/performance curves rather
   than a single binary threshold. Human Delta therefore needs resource and intervention curves,
   not an agent-only win rate.
   Source: https://metr.org/blog/2026-07-21-expenditure-horizon/

4. **Fresh, executable tasks are a control.** SWE-bench-Live couples recent real issues with
   dedicated Docker images and a continuously updated curation pipeline. Freshness reduces
   contamination risk; executable environments make outcomes reproducible.
   Source: https://arxiv.org/abs/2505.23419

5. **Separate task, solver, scorer, sandbox, and record.** The UK AI Security Institute's Inspect
   framework treats datasets, solvers, scorers, sandboxes, and logs as distinct components. This
   is the architectural answer to the false-green class: an agent's own completion narrative is
   never its acceptance test.
   Source: https://inspect.aisi.org.uk/

## Design consequences

- The public object is a **thermometer**, not an autonomous submission factory. It measures how
  far a bounded agent can proceed before correct completion requires human intervention.
- Every run records five separable objects: task identity, execution identity, deployed artifact,
  protected scorer, and human intervention log.
- A green source-tree test is not a green deployed product. The scorer must execute the artifact
  that would actually be delivered.
- Cold onboarding is measured against an exact committed truth contract and a 15-minute ceiling;
  fluent prose is not sufficient.
- The first public metric should be a vector: correct completion, invalid completion claims,
  human minutes, total expenditure, and task difficulty in expert-human minutes.
- The causal P3 ablation remains frozen. These POCs calibrate its instruments; they do not count
  as evidence that SEED helps.

## Immediate POCs

1. **Cold-start comprehension:** a machine-scored contract checks whether a fresh reader recovers
   the mission, boundary, current state, and next action from repository evidence within 15
   minutes.
2. **Deceptive-green evaluator:** an intentionally stale deployable artifact passes a weak
   source-tree check and fails a protected artifact check. The POC passes only when it detects
   both outcomes.

## Boundaries

- No model or harness is graded by its own assertions.
- No live platform action, account action, submission, or publication is in scope.
- Synthetic POCs validate instruments only. They do not support a capability or causal-benefit
  claim.
- An independent cold run is still required before Bonkers P2 can close.
