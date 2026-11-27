---
name: arena
description: "Run parallel independent attempts on a hard design or implementation task, grade them against a rubric, and combine the best parts into one solution. Pass the task and desired deliverable after /arena (spawns multiple subagents; count set by parallel_subagents)."
disable-model-invocation: true
---

# Arena

If the user invokes `/arena` without specifying a task, ask for the task, the deliverable each candidate should produce, and any key constraints before spawning candidates.

Open a todo list with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify and clean up) before launching anything.

## Phase A: Frame

Every candidate receives the same prompt, so the prompt is the contract.

1. State the exact deliverable each candidate must produce.
2. Derive the rubric: 3 to 6 concrete, gradeable criteria for what success looks like on this task. Candidates see only the task; the picker (and optional cross-judge) uses the rubric.
3. Read [`../develop/references/config-and-subagents.md`](../develop/references/config-and-subagents.md) and resolve `parallel_subagents`, `high_effort_model`, and optional `arena_cross_judge` (default `false`) from `develop-config.md`. Comparing competing designs requires at least `2` candidates, so if `parallel_subagents` is `1`, run `2` candidates and note that override once.
4. Give each candidate an isolated output location: a separate git worktree when working in a git repository (copying any uncommitted in-scope working-tree edits or files into each worktree), or an isolated OS temp directory (`$env:TEMP/arena-<slug>/candidate-<n>/` in PowerShell or `%TEMP%\arena-<slug>\candidate-<n>\` in cmd on Windows; `/tmp/arena-<slug>/candidate-<n>/` on macOS and Linux), per [Separate Before Serializing Shared State](../develop/references/principles/separate-before-serializing-shared-state.md).

## Phase B: Fan out

Spawn all candidates concurrently via your coding assistant's subagent tool (see `../develop/references/config-and-subagents.md` Sections 4 and 5). Give each candidate:

- The mandatory kickoff first line `Read <develop-dir>/worker.md before anything else.`
- The task, pointers to shared context files, its isolated output path, and instructions to produce both the deliverable and a short rationale naming alternatives considered and rejected.

Apply the deprecated-model fallback protocol from `../develop/references/config-and-subagents.md` if any configured model is rejected (keeping at least two candidates). If your coding assistant has no subagent tool, execute each candidate sequentially in separate output directories using clean prompts. If a candidate produces no output, proceed with the remaining candidates and note the dropout.

## Phase C: Cross-judge (optional)

Run Phase C only when `arena_cross_judge: true` in `develop-config.md` or explicitly requested by the user.

After Phase B completes, spawn one read-only judge subagent using `high_effort_model` (if a comma-separated list is configured and supported, pick an alternate entry or legacy `arena_judge_model` when available), starting with the mandatory `worker.md` kickoff line. Give it the rubric and neutral candidate path labels (`candidate-1`, `candidate-2`, and so on). Apply the same deprecated-model fallback if the judge model is rejected. The judge scores each candidate on every rubric criterion and recommends a base.

When `arena_cross_judge` is `false`, skip Phase C and score the candidates directly in Phase D.

## Phase D: Pick a base

Read every candidate end to end before deciding. Score each against the rubric criterion by criterion (not on holistic feel), comparing against the cross-judge verdict if Phase C ran. Agreement confirms the pick; disagreement signals bias or an ambiguous rubric.

Pick the base a future maintainer can extend most cleanly without breaking invariants. When two candidates tie, prefer the cleaner boundary or smaller API footprint per [Laziness Protocol](../develop/references/principles/laziness-protocol.md).

## Phase E: Combine the best parts (graft)

Inspect each losing candidate once more for specific strengths worth porting into the base (usually one or two targeted ideas, not large blocks). Integrate each improvement cleanly under one mental model per [Redesign from First Principles](../develop/references/principles/redesign-from-first-principles.md) rather than pasting mechanically.

Apply the synthesized code or document into the active workspace or target branch (checking for conflicting uncommitted edits before overwriting). If all candidates converge on one shape, note the consensus and apply it without combining extra pieces. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging incompatible designs.

## Phase F: Verify and clean up

1. Verify the synthesized deliverable against the real system per [Prove It Works](../develop/references/principles/prove-it-works.md). If verification catches a defect the arena missed, either Phase A missed a requirement or a losing candidate handled it better. Fix the root cause rather than papering over it.
2. Clean up all temporary git worktrees, scratch branches, and temp directories created for candidates once the synthesized deliverable is applied and verified. Confirm no stray worktrees remain.

## Outputs

Return one synthesized deliverable with a short synthesis note naming:

- Chosen base, rationale, and where the final deliverable was written
- Cross-judge verdict (or note that Phase C was skipped)
- Each ported improvement and its source candidate
- What was rejected and why
- Any convergence, dropouts, or model fallback notices
- Verification evidence and confirmation that temporary candidate directories were removed
