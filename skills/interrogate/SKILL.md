---
name: interrogate
description: "Adversarial review of a diff or design where only findings proven by running real code survive. Defaults to your current branch diff, or pass a file, commit, PR, or design doc after /interrogate (spawns parallel reviewers set by parallel_subagents)."
disable-model-invocation: true
---

# Interrogate

Adversaries try to break a change or design. A finding survives only when an actual run proves it. Report verified findings; do not apply fixes unless asked afterward. For downstream cross-module impact analysis, point the user to `/blast-radius`; for comment and suppression cleanup, point them to `/audit-comments`.

## Frame

Use the files, commit, PR, or design document the user names. Otherwise use the current branch diff from its merge base with the repository's default branch (including uncommitted working-tree changes). If there is no named target and the branch diff is empty, ask the user what code, commit, or design they want reviewed.

Restate the intent using the **in-your-own-words** skill from the user's message, commits, and PR description. Ask the user if the intent is unclear.

## Fan out

1. Read [`../develop/references/config-and-subagents.md`](../develop/references/config-and-subagents.md) and resolve `parallel_subagents` (default `2`, minimum `1`) and `high_effort_model` (default `inherit`; accepts a comma-separated list for multi-model review on assistants that support concrete model names) from `develop-config.md`.
2. When reviewing code inside a git repository, give each adversary an isolated git worktree (copying modified and untracked in-scope working-tree files into each worktree) per [Separate Before Serializing Shared State](../develop/references/principles/separate-before-serializing-shared-state.md). For pure design-doc reviews or non-git folders, give each adversary an isolated OS temp directory (`$env:TEMP` in PowerShell or `%TEMP%` in cmd on Windows; `/tmp` on macOS and Linux) for any scratch repro scripts.
3. Spawn all adversary subagents concurrently via your coding assistant's subagent tool (see `../develop/references/config-and-subagents.md` Sections 4 and 5), starting each kickoff with `Read <develop-dir>/worker.md before anything else.` Apply the deprecated-model fallback protocol if any configured model is rejected. If your coding assistant has no subagent tool, run the adversarial pass yourself in an isolated scratch check. Give each adversary the scope, the restated intent, and this brief:

> Break this change. Prove each finding with a run against the real code, such as a failing test, a repro script, or command output that shows the wrong behavior. For a design or plan, run a prototype or probe the current tree. Keep repros in your own isolated worktree or temp directory. Report each finding with a title, the exact command, the output it printed, and the output the intent requires. Leave out anything you did not run. That covers style, naming, structure, and risks that need a future change to matter. No findings is a valid result.

## Verify

Independently verify every reported finding by rerunning its command against the real tree (per [Prove It Works](../develop/references/principles/prove-it-works.md)). Keep a finding only when the output reproduces the failure and the failure violates the restated intent. Drop everything else and merge duplicates that share a root cause.

Adversaries catch different bugs, so keep every verified finding across all reviewers rather than picking one reviewer's list. Clean up all temporary worktrees and scratch directories after verification.

## Output

- **Intent:** the restated intent.
- **Findings:** for each verified finding, the command, observed output, how it breaks the intent, and which reviewers found it. State "no verified findings" when none survive.
- **Dropped:** for each reviewer, the count of dropped findings and why.
- **Model fallbacks (only if triggered):** one-time deprecation notice per `../develop/references/config-and-subagents.md`.
