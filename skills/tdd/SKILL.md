---
name: tdd
description: "Fix a bug or build a focused behavior by writing a failing test first, confirming it fails, then implementing the fix. Pass the bug or expected behavior after /tdd (skips brittle tests when no cheap local test path exists)."
disable-model-invocation: true
---

# Test-driven development (TDD)

When fixing a bug or implementing a focused behavior with a clear, cheap local test path, make the expected behavior executable before changing production code. The goal is a focused test that fails before the change and passes after it.

If the user invokes `/tdd` without naming a bug or expected behavior, ask what behavior or failure they want to lock down with a test first.

Do not force a test when it would be impractical. If the available test would require broad setup, brittle mocks, slow end-to-end infrastructure, production-only state, vague reproduction steps, or large unrelated fixture churn, skip adding a new test and use the closest useful verification instead.

## Workflow

1. **Understand the behavior or bug.** Identify the intended behavior, current behavior, affected path, and smallest observable reproduction.
2. **Choose the narrowest executable check.** Prefer the closest unit, component, integration, or regression test already used for that codepath. If no practical test path is obvious, do not invent heavy infrastructure just to satisfy the workflow.
3. **Write the failing test first.** Add the smallest focused test that would have caught the bug or proves the new requirement. Encode observable behavior, not internal implementation details (see [Test Behavior, Not Implementation](../develop/references/principles/test-behavior-not-implementation.md)).
4. **Run the new test before editing production code.** Confirm it fails for the intended reason. If it passes or fails for an unrelated reason, fix the test or reproduction before touching implementation code.
5. **Implement the smallest fix or change.** Satisfy the intended behavior while preserving nearby contracts.
6. **Rerun the test.** Confirm the new test and related suite now pass.

## If a failing test is impractical

Use the closest executable check instead: a targeted script, reproduction command, browser automation, snapshot comparison, log assertion, or focused integration check.

Prefer no new test over a bad test. A bad test mostly tests mocks, mirrors internal implementation details, depends on timing or unrelated global state, needs expensive infrastructure for a small change, or would be deleted immediately after proving the fix.

## Guardrails

- Do not change existing tests merely to match a wrong implementation.
- Do not weaken existing assertions unless the expected behavior has genuinely changed and the reason is clear.
- Keep the new test focused on the target behavior. Avoid broad fixture churn or unrelated coverage expansion.
- If a bug is flaky, make the test deterministic where possible and document the signal being locked down.
- If a bug exposes a broader class of failures, land the focused regression path first, then consider sibling coverage.

## Final response

Report concrete verification evidence alongside the outcome:

- Name the failing-before test or executable check and the failure output it produced.
- Name the passing-after test run and any nearby validation performed.
- If failing-before evidence could not be demonstrated, state why and describe the closest check used instead.
