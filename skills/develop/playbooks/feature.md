### Feature

**You own the design. Plan, review, verify.**

1. Trace the affected subsystem and existing patterns.
2. Run **architect** when the change crosses a function or module boundary to settle types, signatures, and ownership first (read `references/principles/foundational-thinking.md` and `references/principles/model-the-domain.md`).
3. Write a brief decomposition check before editing:
   - **Blocking prerequisites:** shared types, schemas, or scaffolds that must land first.
   - **Parallel vs. sequential work:** isolate independent files/workstreams; keep shared writes sequential (read `references/principles/separate-before-serializing-shared-state.md`).
   - **Delegation choice:** state whether you are implementing directly or delegating based on `delegation_policy` in `develop-config.md`.
4. **Implement.**
   - When `delegation_policy` is `always-delegate`, or `adaptive` for multi-file, cross-module, or context-heavy changes, delegate implementation to a `develop-agent` subagent (using `code_delegate_model`) with exact file paths, named data shape, organizing structure, and verification criteria.
   - When `delegation_policy` is `single-agent`, or `adaptive` for a small, localized change, implement directly and perform a strict independent diff review before verifying.
   - When the implementation admits genuinely competing architectural shapes and the stakes warrant it, delegate via **arena** so multiple candidates surface tradeoffs.
   - Port improvements across all affected callers and verify each.
5. **Verify on the matching surface.** Exercise the feature on the real app, CLI, API, or test suite (read `references/principles/prove-it-works.md`). "It compiles" or an inconclusive run is not a pass.
6. **Clean and sequence commits.** Self-review for dead code and slop, run **no-comments**, and organize into small, verifiable commits (read `references/principles/sequence-verifiable-units.md`).
7. If the design or risk is contested, run **interrogate** before shipping.
8. Run **Opening a PR** when a PR is requested.

**Reply:** what you built, design choices and tradeoffs, principles applied, verification evidence, and any open decisions.
