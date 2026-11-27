# Bug fix

**You own this task. Plan, review, verify.** Stay in the lead and keep changes strictly justified by runtime evidence.

Be scientific. Every shipped line must trace to runtime evidence. Speculative guards that "might help" are hypotheses, not fixes, and do not ship. When evidence refutes a hypothesis, revert what it motivated.

1. **Reproduce first.** Reproduce the defect yourself on the affected runtime path using the project's `verify-*` skill or native local tooling (test runner, CLI, browser automation, or HTTP request). Ask the user to reproduce only when a concrete local limitation prevents reaching the target, and state why.
2. **Isolate the root cause.** Form candidate hypotheses and narrow them systematically until one survives (read [Fix Root Causes](../references/principles/fix-root-causes.md)). Use **why** for regression history when helpful. Add temporary instrumentation or logging when runtime state is unclear, then remove it before committing. Confirm the mechanism with runtime evidence before writing a fix.
3. **Lock down a failing test (when cheap) and implement the fix.**
   - If the fix crosses a public or shared interface or module boundary, run **architect** first.
   - When a cheap, deterministic local test path exists, use **tdd** to write and confirm a failing regression test before editing production code (read [Test Behavior, Not Implementation](../references/principles/test-behavior-not-implementation.md)). Skip brittle mock tests when a direct executable check is stronger.
   - Follow `delegation_policy` and subagent rules in [`../references/config-and-subagents.md`](../references/config-and-subagents.md):
     - If delegating (`always-delegate`, or `adaptive` on a multi-file or high-risk fix), spawn an implementation delegate subagent (using `medium_effort_model`) with the exact scope, confirmed root cause, any TDD requirement, and success criteria.
     - If executing directly (`single-agent`, or `adaptive` on a small focused fix), apply the smallest justified edit directly and perform an explicit fresh diff self-review afterward.
4. **Verify on the same runtime path.** Re-run the original reproduction and any regression test, confirming both now pass (read [Prove It Works](../references/principles/prove-it-works.md)). Unit tests alone do not prove absence of an integration or runtime defect unless that is the failing path.
5. **Sequence the commits.** Organize commits in proving order so any failing regression test lands before or alongside the fix cleanly (read [Sequence Verifiable Units](../references/principles/sequence-verifiable-units.md)).
6. **Clean and ship.** Run **audit-comments** on the diff, then run [Opening a PR](opening-a-pr.md) when a PR is requested.

**Reply:** what was broken, confirmed root cause, minimal fix, principles applied, and verbatim before-and-after verification output.
