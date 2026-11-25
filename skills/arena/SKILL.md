---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, and graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial design or artifact could lock in the wrong shape."
disable-model-invocation: true
---

# Arena

Open a todo list with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before launching anything.

## Phase A: Frame

Every candidate receives the same prompt, so the prompt is the contract.

1. State the artifact each candidate must produce.
2. Derive the rubric: 3-6 concrete, gradeable criteria for what success looks like on *this* task. Candidates only see the task; the picker (and optional cross-judge) uses the rubric.
3. Read `develop-config.md` (`.agents/develop-config.md`, `~/.claude/rules/develop-config.md`, or `~/.agents/develop-config.md`) for panel configuration:
   - `arena_candidates`: number of parallel candidates to spawn (default `2`, minimum `2`).
   - `arena_models`: comma-separated list of models/tiers, or `inherit-parent` (default `inherit-parent`). If fewer models are listed than `arena_candidates`, assign remaining candidates `inherit-parent`.
   - `arena_cross_judge`: `true` or `false` (default `false`).
   - `arena_judge_model`: model/tier for the optional cross-judge (default `inherit-parent`).
   - For `inherit-parent` (or `auto`), omit any explicit model override so the subagent uses the active chat model. If your harness rejects a configured model slug, fall back to the closest valid tier or omit the model parameter, keep at least two candidates, and note the fallback once.
4. Give each candidate its own isolated output location (a separate git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`), following `../develop/references/principles/separate-before-serializing-shared-state.md`.

## Phase B: Fan out

Spawn all `arena_candidates` subagents concurrently using your harness's subagent tool (see `docs/harness.md`), giving each:
- The first line `Read <develop-dir>/worker.md before anything else.` when running under `/develop`.
- The task, pointers to shared context files, its isolated output path, and instructions to produce both the artifact and a short rationale naming alternatives considered and rejected.

If your harness has no subagent tool, execute each candidate sequentially in separate output directories using clean prompts. If a candidate produces no output, proceed with the remaining candidates and note the dropout.

## Phase C: Cross-judge (optional)

Run Phase C only when `arena_cross_judge: true` in `develop-config.md` or explicitly requested by the user.

After Phase B completes, spawn one read-only judge subagent using `arena_judge_model` (preferring a different model family than the parent when configured and supported by your harness). Give it the rubric and neutral candidate path labels (`candidate-1`, `candidate-2`, ...). The judge scores each candidate on each rubric criterion and recommends a base.

When `arena_cross_judge` is `false`, skip Phase C and score the candidates directly in Phase D.

## Phase D: Pick a base

Read every candidate end to end before deciding. Score each against the rubric criterion by criterion (not on holistic feel), comparing against the cross-judge verdict if Phase C ran. Agreement confirms the pick; disagreement signals bias or an ambiguous rubric.

Pick the base a future maintainer can extend most cleanly without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller surface, per `../develop/references/principles/laziness-protocol.md`.

## Phase E: Graft

Inspect each losing candidate once more for specific strengths worth porting into the base (usually one or two targeted ideas, not large blocks). Integrate each graft cleanly under one mental model per `../develop/references/principles/redesign-from-first-principles.md` rather than pasting mechanically.

If all candidates converge on one shape, note the consensus and ship it without grafting. If they wildly diverge, Phase A was under-specified: reframe and re-run rather than averaging incompatible designs.

## Phase F: Verify

Verify the synthesized artifact against the real system per `../develop/references/principles/prove-it-works.md`. If verification catches a defect the arena missed, either Phase A missed a requirement or a losing candidate handled it better. Fix the root cause rather than papering over it.

## Outputs

Return one synthesized artifact with a short synthesis note naming:
- Chosen base and rationale
- Cross-judge verdict (or note that Phase C was skipped)
- Each graft and its source candidate
- What was rejected and why
- Any convergence, dropouts, or model fallbacks
- Verification evidence
