# Laziness Protocol

Apply when deciding where code should live, sizing a diff, refactoring, or tempted to add abstractions, copies, or new layers.

Code is a maintenance liability, not an asset — every new line carries a lasting commitment to maintain.

- **Ask "where does this belong?" first.** Before writing code, identify the single right owner for the responsibility. If it clearly belongs in the current component, implement it cleanly here without wasting effort searching elsewhere. If it belongs in a shared library or cross-cutting utility already in the stack, check that home and reuse, depend on, or upstream the change instead of reimplementing or forking.
- **Keep one source of truth.** Avoid creating diverging forks, copy-pasted helpers, duplicated constants, or mirrored documentation across repositories. Consolidate decisions behind one authoritative source.
- **Minimize the diff.** Make the smallest change that solves the problem cleanly. Fewer clear lines beat speculative boilerplate.
- **Bias toward deletion.** Removing dead code, stale overrides, and unnecessary indirection is progress.
