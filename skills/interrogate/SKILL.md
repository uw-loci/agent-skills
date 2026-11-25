---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Adversaries try to break a change or design, and only findings proven by a run survive."
disable-model-invocation: true
---

# Interrogate

Adversaries try to break a change or design. A finding survives only when an actual run proves it. Report verified findings; do not apply fixes unless asked afterward.

## Frame

The scope is whatever the user names. Otherwise it is the current branch diff from its merge base with the base branch, including uncommitted working-tree changes. Restate the intent using the **in-your-own-words** skill from the user's message, commits, and PR description. Ask the user if the intent is unclear.

## Fan out

1. Read `develop-config.md` (`.agents/develop-config.md`, `~/.claude/rules/develop-config.md`, or `~/.agents/develop-config.md`) for reviewer configuration:
   - `interrogate_reviewers`: number of adversary subagents to spawn (default `2`, minimum `1`).
   - `interrogate_models`: comma-separated list of models/tiers, or `inherit-parent` (default `inherit-parent`). If fewer models are listed than `interrogate_reviewers`, assign remaining reviewers `inherit-parent`.
   - For `inherit-parent` (or `auto`), omit any explicit model override so the subagent inherits the active chat model. If your harness rejects a configured model slug, fall back to the closest valid tier or omit the model parameter and note the fallback once.
2. Give each adversary its own isolated git worktree (copying uncommitted changes in scope into each worktree) per `../develop/references/principles/separate-before-serializing-shared-state.md`.
3. Spawn all `interrogate_reviewers` subagents concurrently using your harness's subagent tool (see `docs/harness.md`). If your harness has no subagent tool, run the adversarial pass yourself in an isolated scratch check. Give each adversary the scope, the restated intent, and this brief:

> Break this change. Prove each finding with a run against the real code, such as a failing test, a repro script, or command output that shows the wrong behavior. For a design or plan, run a prototype or probe the current tree. Keep repros in your own worktree. Report each finding with a title, the exact command, the output it printed, and the output the intent requires. Leave out anything you did not run. That covers style, naming, structure, and risks that need a future change to matter. No findings is a valid result.

## Verify

Independently verify every reported finding by rerunning its command against the real tree (per `../develop/references/principles/prove-it-works.md`). Keep a finding only when the output reproduces the failure and the failure actually violates the restated intent. Drop everything else and merge duplicates that share a root cause.

Adversaries catch different bugs, so keep every verified finding across all reviewers rather than picking one reviewer's list. Clean up any temporary worktrees after verification.

## Output

- **Intent:** the restated intent.
- **Findings:** for each verified finding, the command, observed output, how it breaks the intent, and which reviewer(s) found it. State "no verified findings" when none survive.
- **Dropped:** for each reviewer, the count of dropped findings and why.
