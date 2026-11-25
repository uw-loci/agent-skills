# Test Behavior, Not Implementation

Apply whenever writing, updating, or reviewing tests.

A test makes a claim about what callers or users can observe through the public interface: return values, error types, persisted state, and observable side effects. Private helpers, internal call order, and intermediate representations are implementation details.

Judge every test against two checks:

- **Break the behavior** (wrong output, skipped or duplicated side effect). If the test still passes, it proves nothing.
- **Refactor the internals** while preserving observable behavior. If the test fails, it is coupled to implementation details.

Keep tests that catch the first and survive the second. Drive code through its public interface with concrete inputs and expected values derived from requirements, not computed by the code under test.
