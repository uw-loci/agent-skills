# Laziness Protocol

Apply when refactoring, sizing a diff, or tempted to add abstractions, layers, or extra parameters.

- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth and pass the result cleanly.
- **Minimize the diff.** Make the smallest change that solves the problem. Fewer lines beat speculative boilerplate.
- **Bias toward deletion.** Removing dead code and unnecessary indirection is progress.
