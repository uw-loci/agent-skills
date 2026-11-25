# Guard the Context Window

Apply when a task involves large log outputs, big diffs, broad codebase searches, or multi-step fan-out work.

Context bloat degrades reasoning quality, forces lossy compaction, and inflates token cost.

- Route bulky exploration, log scanning, or isolated multi-file edits to subagents when `delegation_policy` permits, and return concise summaries plus file pointers to the main session.
- Pass file paths and narrow scopes rather than pasting whole files into subagent briefs.
- Cap phase scope and keep outputs concise so every turn stays focused on active decisions.
