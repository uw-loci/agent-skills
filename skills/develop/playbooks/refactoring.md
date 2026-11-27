### Refactoring

**You own the contract. The structure changes. The behavior does not.**

If cleanup exposes a real bug or missing feature, split it out and ship the structural change first against the pinned contract.

1. **Pin the behavior contract first.** Trace the affected subsystem and verify existing test coverage. If the area lacks behavior coverage, write a characterization test, snapshot, or equivalence check before moving structure (read `references/principles/test-behavior-not-implementation.md`). Type check and lint alone are not a behavior pin.
2. **Name the target shape.** Identify the missing structure (read `references/principles/model-the-domain.md`, `references/principles/foundational-thinking.md`, `references/principles/redesign-from-first-principles.md`). Keep boring local code as-is if reshaping adds indirection without removing branches or invalid states. Run **architect** when the target crosses module boundaries.
3. **Subtract before adding.** Delete dead code, collapse one-caller wrappers, drop redundant validators, and remove orphan references before introducing the new shape (read `references/principles/minimize-reader-load.md` and `references/principles/laziness-protocol.md`). Revert speculative cleanups that do not earn their place.
4. **Move in small behavior-preserving steps.** Keep the behavior pin green at every step.
   - For **internal APIs or `0.x` incubating libraries**, migrate every caller and delete the legacy API in the same wave rather than keeping throwaway compatibility shims.
   - For **mature (`>= 1.0`) public library APIs**, preserve SemVer backward compatibility (read `references/principles/reproducible-immutable-artifacts.md`): keep existing public signatures working via `@Deprecated` delegating wrappers with migration guidance, and check whether the `-SNAPSHOT`/`.dev0` version needs advancing if new public API was added.
   - Spot-check renames across strings, config, and docs. Honor `delegation_policy` from `develop-config.md` for mechanical multi-file edits (using `medium_effort_model` per `SKILL.md` model and deprecation fallback rules).
5. **Prove behavior is unchanged.** Run the behavior pin and an end-to-end check on the real artifact (read `references/principles/prove-it-works.md`).
6. **Confirm reader load dropped.** If the diff does not make the code simpler to trace or maintain, revert it.
7. **Clean and sequence commits.** Run **no-comments**, organize commits in proving order (pin, subtraction, reshape, cleanup per `references/principles/sequence-verifiable-units.md`), and run **Opening a PR** when a PR is requested.

**Reply:** structure changed, behavior pin used, equivalence proof, reader-load delta, and anything intentionally left untouched or reverted.
