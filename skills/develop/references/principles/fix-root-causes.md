# Fix Root Causes

Apply when debugging defects or reviewing workarounds.

Fix the fault, not the place where it surfaced. The root cause is the first place the system made a wrong decision or failed to handle a legitimate state.

- Reproduce first. Keep asking "why" until the answer is a concrete wrong decision in code. When runtime state is unclear, instrument and observe it directly.
- **Reduce data and isolate state.** When debugging failures on large scientific images or multi-stage pipelines, shrink the input to a minimal reproducible fixture or serialize intermediate state before bisecting.
- Ask whether the state that triggered the symptom is legitimate. If it is, handle it cleanly where the code broke. If it should never exist, a guard there hides the bug. Find what produced the invalid state instead. Swallowed errors, retries, clamped values, and defensive guards often conceal root causes.
- **Attack the premise when stuck.** If two or more fixes sharing one assumption fail the same check, stop patching. Write the shared premise down in one sentence and run an observation that directly tests whether that premise is true.
- Fix the pattern across scope, not only one instance.
