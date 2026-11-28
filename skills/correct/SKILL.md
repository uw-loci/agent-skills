---
name: correct
description: "Turn recurring agent mistakes in this repository into permanent checks (architecture, types, lint, or tests) instead of extra prompt prose. Pass a specific mistake to encode or run /correct to audit recent history; proposes changes for approval before editing."
disable-model-invocation: true
---

# Correct

When the user keeps correcting agents in this repository for the same mistakes, change the repository so future agents cannot repeat them.

Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Design the repository so a change that looks right from one file is right for the whole repository.

## 1. Identify the mistake class

Choose the matching entry mode:

- **Specific correction supplied:** If the user names a mistake they just caught (or points to one in this session), focus on that mistake class first and check git history to see if it has occurred before.
- **Repository audit (bare `/correct`):** Read recent commits, reverts, review comments, repo agent instruction files, and comments that explain workarounds. Group repeated mistakes into classes. A class counts once it has happened twice. If no clear repeated mistake classes appear, report that and ask the user which mistake they want to encode.

For durable workflow lessons that belong in the skill files themselves rather than repository code, tests, or lint checks, point the user to `/reflect`.

## 2. Pick the highest enforcement level that works

For each mistake class, choose the strongest structural fix possible:

1. **Eliminate it with architecture.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old ways and dead code an agent would copy.
2. **Enforce it with types or automated checks.** Make the invalid state fail to compile. If bad code still compiles, add a lint rule or CI check whose error message names the file, type, or function to use instead. If the pattern is already common, fail only when a change adds new instances.
3. **Test the behavior.** Fix or delete any test that still passes when the checked behavior breaks, or that fails when only internals change.
4. **Write docs or agent rules last, only for judgment calls.** Prose rules are the weakest defense because nothing fails when an agent skips them.

## 3. Propose before editing

Before editing production code, CI, instruction files, or creating git commits, present a concise plan listing:

- Each mistake class and its evidence (commits, files, or session correction)
- The chosen enforcement level and why a higher level does not fit
- The exact files you plan to edit and how you will prove each check fails on a real past mistake

Wait for user approval before applying edits or creating commits.

## 4. Fix, prove, and update the rule table

Once approved:

1. Implement the approved classes in small, single-purpose changes (one commit per class if committing). Prove each new check fails against a real past mistake (or minimal reproduction) and passes after the fix. Run the same command locally and in CI. Put any narrow exception on the offending line with a reason, an expiry date, and human approval.
2. Track rules in the repository's existing agent instruction file (for example, `CLAUDE.md`, `.github/copilot-instructions.md`, `GEMINI.md`, or a coding-rules `AGENTS.md`; do not overwrite an installer-only `AGENTS.md` without asking). Pair each rule with what enforces it. If a rule already existed with no enforcement and repeated, upgrade it to a higher level in the same change. Drop a rule once its mistake can no longer happen.

**Reply:** each mistake class with its evidence, the enforcement level chosen, why a higher level did not work, and verification output (or the proposed plan awaiting approval).
