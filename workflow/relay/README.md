# relay -- cross-harness context relay buffer

Harness-neutral. Any agent that can read files and run git can use this. Nothing
here requires a slash command, a skill, or an MCP server.

## What this is

Two or three agents in different harnesses (Claude Code, Codex, ...) work the same
repo on staggered context lifecycles. Rather than one handing off to the next, they
orbit: each keeps its own belief cell, they compare cheap digests, and they
reconcile only where they disagree.

## The rules that make it work

1. ANCHOR TO THE REPO, NOT TO EACH OTHER. Every cycle, re-derive from git and from
   the verify command before comparing beliefs. Two agents agreeing is not evidence
   if both inherited the same wrong summary.
2. ROLE BY REMAINING CONTEXT. The freshest agent explores (wide reads, searches,
   debug loops). The most loaded agent judges (reviews, decides, holds the why).
   Run `relay.py roles`. As the fresh one loads up, the roles rotate.
3. DIGESTS, NOT STATE. Compare with `relay.py sync`, which hashes each dimension
   separately. Spend tokens only on dimensions that differ.
4. OLD OWNS WHY, FRESH OWNS WHAT. On a conflict about intent or rejected
   alternatives, the older agent wins. About current file state, the fresher wins.
   About a fact, neither wins -- run the verify command; reality wins.
5. PULL, NOT PUSH. A cell holds pointers, not pasted content. Let the reader decide
   what to spend its context on.

## Cycle

    python scripts/relay.py stamp <me> --context 0.55   # refresh my meta
    python scripts/relay.py check <me>                  # gate my own cell
    python scripts/relay.py sync                        # where do we differ?
    ... reconcile only the CONFLICT dimensions, anchored on the repo ...
    python scripts/relay.py resolve --dim "State" --winner <agent|repo> --note "..."

## Does this pay?

`relay.py report` reads divergence.jsonl and answers it. If after ~20 cycles the
agents rarely diverged, or diverged only on trivia, the error correction bought
nothing -- drop to a single-agent handoff and keep the orbit for high-stakes work.
That is the question this prototype exists to settle.
