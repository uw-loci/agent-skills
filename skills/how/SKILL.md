---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
disable-model-invocation: true
---

# How

Explore the codebase to answer "how does X work?" questions.

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

## 1. Explain

Read `develop-config.md` (`.agents/develop-config.md`, `~/.claude/rules/develop-config.md`, or `~/.agents/develop-config.md`) for `low_effort_model` (default `inherit`; legacy fallback `research_model`) and `delegation_policy`.

When `delegation_policy` is not `single-agent` and your coding assistant has a subagent tool (see `docs/harness.md`), spawn one read-only research subagent (using `low_effort_model`, omitting the model parameter for `inherit` or legacy `inherit-parent` / `auto`) to explore and explain in one pass. Otherwise explore and write the explanation directly in the main session.

**Deprecated or unsupported model fallback:** If your coding assistant rejects the configured model value, never retry the rejected value. Fall back immediately to `inherit` to complete the walkthrough, and include a one-time deprecation notice in Step 2 naming the active `develop-config.md` path, the config key, the rejected value, the valid model values accepted by your assistant, and an offer to update `develop-config.md` and re-run Suite 3 Check 5 of `docs/validation.md`. Do not edit `develop-config.md` without user confirmation.

Use this brief:

> You are writing an architectural explanation for a senior engineer. Explore the codebase and write an explanation that a senior engineer unfamiliar with this area could read and walk away with a solid mental model. Cite concrete file paths and symbols so they understand the architecture well enough to start working in it confidently. You have read-only access to the codebase.

## 2. Present

Present the explanation clearly. Light edits for clarity or context from the conversation are fine; do not dilute concrete file citations. Include the one-time deprecation notice from Step 1 if a configured model was rejected.
