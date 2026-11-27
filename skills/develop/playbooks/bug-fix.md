### Bug fix

**You own this task. Plan, review, verify.** Stay in the lead and keep changes strictly justified by runtime evidence.

Be scientific. Every shipped line must trace to runtime evidence. Speculative guards that "might help" are hypotheses, not fixes, and do not ship. When evidence refutes a hypothesis, revert what it motivated.

1. **Reproduce first.** Reproduce the defect yourself on the matching surface using the project's `verify-*` skill or native local tooling (test runner, CLI, browser automation, HTTP request). Ask the user to reproduce only when a concrete local limitation prevents reaching the target, and state why.
2. **Isolate the root cause.** Form candidate hypotheses and narrow them systematically until one survives (read `references/principles/fix-root-causes.md`). Use **why** for regression history when helpful. Add temporary instrumentation or logging when runtime state is unclear, then remove it before committing. Confirm the mechanism with runtime evidence before writing a fix.
3. **Plan and implement the fix.** If the fix crosses a function or module boundary, run **architect** first. Follow `delegation_policy` from `develop-config.md`:
   - If delegating (`always-delegate`, or `adaptive` on a multi-file/high-risk fix), spawn a `develop-agent` (using `medium_effort_model` per `SKILL.md` model and deprecation fallback rules) with the exact scope, confirmed root cause, and success criteria.
   - If executing directly (`single-agent`, or `adaptive` on a small focused fix), apply the smallest justified edit directly and perform an explicit fresh diff self-review afterward.
4. **Verify on the same surface.** Re-run the original reproduction and confirm it now passes (read `references/principles/prove-it-works.md`). Unit tests alone do not prove absence of an integration or runtime defect unless that is the failing surface.
5. **Sequence the commits.** When there is a cheap, deterministic local test path, use **tdd** so the failing regression test lands before or alongside the fix cleanly (read `references/principles/sequence-verifiable-units.md` and `references/principles/test-behavior-not-implementation.md`). Skip brittle mock tests when a direct executable check is stronger.
6. **Clean and ship.** Run **no-comments** on the diff, then run **Opening a PR** when a PR is requested.

**Reply:** what was broken, confirmed root cause, minimal fix, and verbatim before/after verification output.
