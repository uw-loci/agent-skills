---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
disable-model-invocation: true
---

# How

Explore the codebase to answer "how does X work?" questions.

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

## 1. Explain

Read `develop-config.md` (`.agents/develop-config.md`, `~/.claude/rules/develop-config.md`, or `~/.agents/develop-config.md`) for `research_model` (default `inherit-parent`) and `delegation_policy`.

When `delegation_policy` is not `single-agent` and your harness has a subagent tool (see `docs/harness.md`), spawn one read-only research subagent (using `research_model`, omitting the model parameter for `inherit-parent`) to explore and explain in one pass. Otherwise explore and write the explanation directly in the main session.

Use this brief:

> You are writing an architectural explanation for a senior engineer. Explore the codebase and write an explanation that a senior engineer unfamiliar with this area could read and walk away with a solid mental model. Cite concrete file paths and symbols so they understand the architecture well enough to start working in it confidently. You have read-only access to the codebase.

## 2. Present

Present the explanation clearly. Light edits for clarity or context from the conversation are fine; do not dilute concrete file citations.
