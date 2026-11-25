### Opening a PR

Invoked at the end of code-writing playbooks when opening a pull request.

1. **Isolate and review.** Work from a clean branch or git worktree off the base branch, keeping unrelated edits out. Rebase or organize into small, logical, verifiable commits.
2. **Clean the diff.** Self-review the full diff to remove dead code, stray debug logs, and AI slop. Run **no-comments** if not already run in this wave.
3. **Write a crisp PR title and body.** Apply **technical-writing** and **unslop**:
   - **Title:** `type(scope): subject`, naming a real symbol or area when helpful.
   - **Body:** A one-minute briefing under 40 lines using these `##` headings in order (drop any empty section):
     - `## Why`
     - `## What changed`
     - `## Scope`
     - `## Tradeoffs` (only rejected alternatives a reviewer would otherwise ask about)
     - `## Blast Radius`
     - `## Verification`
   - Link verbose logs or long tables instead of pasting them inline.
4. **Open ready.** Stack follow-up PRs by base branch. Open PRs ready for review (not draft unless requested) using `gh pr create` or your harness's forge tool.
