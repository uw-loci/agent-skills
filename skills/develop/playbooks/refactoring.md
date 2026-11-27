# Refactoring

**You own the contract. The structure changes. The behavior does not.**

If cleanup exposes a real bug or missing feature, split it out and ship the structural change first against the pinned contract.

1. **Pin the behavior contract first.** Trace the affected subsystem and verify existing test coverage. If the area lacks behavior coverage, write a test that locks down current observable outputs (a characterization test, snapshot, or equivalence check) before moving structure (read [Test Behavior, Not Implementation](../references/principles/test-behavior-not-implementation.md)). Type check and lint alone are not a behavior pin.
2. **Name the target shape.** Identify the missing structure (read [Model the Domain](../references/principles/model-the-domain.md), [Foundational Thinking](../references/principles/foundational-thinking.md), and [Redesign from First Principles](../references/principles/redesign-from-first-principles.md)). Keep boring local code as-is if reshaping adds indirection without removing branches or invalid states. Run **architect** when the target crosses module boundaries.
3. **Subtract before adding.** Delete dead code, collapse one-caller wrappers, drop redundant validators, and remove orphan references before introducing the new shape (read [Minimize Reader Load](../references/principles/minimize-reader-load.md) and [Laziness Protocol](../references/principles/laziness-protocol.md)). Revert speculative cleanups that do not earn their place.
4. **Move in small behavior-preserving steps.** Keep the behavior pin green at every step.
   - For **internal APIs or `0.x` incubating libraries**, migrate every caller and delete the legacy API in the same wave rather than keeping throwaway compatibility shims.
   - For **mature (`>= 1.0`) public library APIs**, preserve SemVer backward compatibility (read [Reproducible, Immutable Artifacts](../references/principles/reproducible-immutable-artifacts.md)): keep existing public signatures working via `@Deprecated` delegating wrappers with migration guidance, and check whether the `-SNAPSHOT` or `.dev0` version needs advancing if new public API was added.
   - Spot-check renames across strings, config, and docs. Honor `delegation_policy` and subagent rules in [`../references/config-and-subagents.md`](../references/config-and-subagents.md) for mechanical multi-file edits (using `medium_effort_model`).
5. **Prove behavior is unchanged.** Run the behavior pin and an end-to-end check on the real artifact (read [Prove It Works](../references/principles/prove-it-works.md)).
6. **Confirm reader load dropped.** If the diff does not make the code simpler to trace or maintain, revert it.
7. **Clean and sequence commits.** Run **audit-comments**, organize commits in proving order (pin, subtraction, reshape, cleanup per [Sequence Verifiable Units](../references/principles/sequence-verifiable-units.md)), and run [Opening a PR](opening-a-pr.md) when a PR is requested.

**Reply:** structure changed, behavior pin used, equivalence proof, reader-load delta, principles applied, and anything intentionally left untouched or reverted.
