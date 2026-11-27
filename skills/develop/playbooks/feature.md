# Feature

**You own the design. Plan, review, verify.**

1. Trace the affected subsystem and existing patterns.
2. Run **architect** when the change crosses a public or shared interface or module boundary to settle types, signatures, and ownership first (read [Foundational Thinking](../references/principles/foundational-thinking.md), [Model the Domain](../references/principles/model-the-domain.md), [Boundary Discipline](../references/principles/boundary-discipline.md), and [Accessible by Design](../references/principles/accessible-by-design.md) for user-facing commands, CLIs, GUIs, or public APIs).
3. Write a brief decomposition check before editing:
   - **Blocking prerequisites:** shared types, schemas, or scaffolds that must land first.
   - **Parallel versus sequential work:** isolate independent files and workstreams; keep shared writes sequential (read [Separate Before Serializing Shared State](../references/principles/separate-before-serializing-shared-state.md)).
   - **Delegation choice:** state whether you are implementing directly or delegating based on `delegation_policy` in [`../references/config-and-subagents.md`](../references/config-and-subagents.md) (read [Guard the Context Window](../references/principles/guard-the-context-window.md)).
4. **Implement.**
   - When `delegation_policy` is `always-delegate`, or `adaptive` for multi-file, cross-module, or context-heavy changes, delegate implementation to a subagent (using `medium_effort_model` per `../references/config-and-subagents.md`) with exact file paths, named data shape, organizing structure, and verification criteria.
   - When `delegation_policy` is `single-agent`, or `adaptive` for a small, localized change, implement directly and perform a strict independent diff review before verifying.
   - When the implementation admits genuinely competing architectural shapes and the stakes warrant it, use **arena** so multiple candidates test the tradeoffs. Under `single-agent`, ask the user first and note the parallel token cost before launching **arena**.
   - Port improvements across all affected callers and verify each.
5. **Verify on the real target.** Exercise the feature on the real app, CLI, API, or test suite (read [Prove It Works](../references/principles/prove-it-works.md)). "It compiles" or an inconclusive run is not a pass.
6. **Clean and sequence commits.** Self-review for dead code and filler, run **audit-comments**, and organize into small, verifiable commits (read [Sequence Verifiable Units](../references/principles/sequence-verifiable-units.md)).
7. If the design or risk is contested, run **interrogate** before shipping (under `single-agent`, offer **interrogate** and ask first rather than launching parallel reviewers silently).
8. Run [Opening a PR](opening-a-pr.md) when a PR is requested.

**Reply:** what you built, design choices and tradeoffs, principles applied, verification evidence, and any open decisions.
