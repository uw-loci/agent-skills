# Opening a PR

Invoked at the end of code-writing playbooks when opening a pull request.

1. **Isolate and review.** Work from a clean branch or git worktree off the base branch, keeping unrelated edits out. Organize work into small, logical, verifiable commits. Rebase only local, unpushed branches; never rewrite shared or pushed history (read [Reproducible, Immutable Artifacts](../references/principles/reproducible-immutable-artifacts.md)).
2. **Clean the diff.** Self-review the full diff to remove dead code, stray debug logs, and AI writing filler. Run **audit-comments** if not already run in this wave.
3. **Write a crisp PR title and body.** Apply **technical-writing** and **unslop**:
   - **Title:** Conventional commit format `type(scope): subject` (for example, `fix(angles): preserve 3D axis order`), naming a real symbol or area when helpful.
   - **Body:** A one-minute briefing under 40 lines using these `##` headings in order (drop any empty section):
     - `## Why`
     - `## What changed`
     - `## Scope`
     - `## Tradeoffs` (only rejected alternatives a reviewer would otherwise ask about)
     - `## Blast radius`
     - `## Verification`
   - Link verbose logs or long tables instead of pasting them inline.
4. **Confirm and open ready.** If the user did not explicitly ask to push and open a pull request yet, present the proposed branch, title, and PR body and ask for confirmation first. Stack follow-up PRs by base branch. Open PRs ready for review (not draft unless requested) using the GitHub or GitLab CLI (such as `gh pr create`) or your hosting tool.
