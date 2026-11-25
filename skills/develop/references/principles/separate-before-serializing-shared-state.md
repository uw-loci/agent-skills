# Separate Before Serializing Shared State

Apply when concurrent actors (parallel subagents, workers, or processes) might write to the same file, branch, worktree, key, or state object.

First ask whether actors actually need one shared target or are producing independent outputs.

- Default to giving each actor its own isolated output path, git worktree, branch, or key, and merge only where results are read.
- Two workers updating different fields inside one shared file is still shared mutation.
- Serialize access structurally (lockfile, single writer, sequential phases, atomic compare-and-swap) only when a single shared writer is a real domain invariant. Prose instructions are not concurrency control.
