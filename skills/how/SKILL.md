---
name: how
description: "Explain how a subsystem works with cited file paths and symbols, or answer where new code belongs. Pass a subsystem, file, or ownership question after /how (use /why for design history)."
disable-model-invocation: true
---

# How

Explore the codebase to answer "how does X work?" or "where should X live?" questions.

If the user invokes `/how` without naming a subsystem, file, or question, ask what part of the codebase they want explained before exploring. If a target is given but mildly ambiguous, state your interpretation and explore so the user can redirect if needed. If the user asks why a design decision was made in git history or wants a guided plain-language walkthrough, point them to `/why` or `/teach`.

## 1. Explain

Read [`../develop/references/config-and-subagents.md`](../develop/references/config-and-subagents.md) and resolve `low_effort_model` (default `inherit`) and `delegation_policy` from `develop-config.md`.

When `delegation_policy` is not `single-agent` and your coding assistant has a subagent tool, spawn one read-only research subagent (using `low_effort_model`, starting with the mandatory `Read <develop-dir>/worker.md before anything else.` kickoff line, and following the deprecated-model fallback protocol if a configured model is rejected) to explore and explain in one pass. Otherwise explore and write the explanation directly in the main session.

Use this brief:

> You are writing a clear architectural explanation for a developer unfamiliar with this area. Explore the codebase and produce a concise mental model covering overview, key components, runtime flow, and gotchas. Cite concrete file paths and symbols so the reader can start working in this area confidently. You have read-only access to the codebase.

## 2. Present

Present the explanation clearly. Light edits for clarity or context from the conversation are fine; do not dilute concrete file citations. Include the one-time deprecation notice from Step 1 if a configured model was rejected.
