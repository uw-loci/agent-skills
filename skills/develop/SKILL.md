---
name: develop
description: Rigorous engineering workflow router for investigations, bug fixes, features, refactoring, prototypes, multi-phase plans, and PRs. Matches tasks to playbooks, applies core engineering principles, routes to specialist skills, and respects team model and delegation config. Use for /develop or requests for rigorous, verified engineering work.
disable-model-invocation: true
---

# Develop

Sibling skills live at `../<name>/SKILL.md` relative to this file. When delegating to a `develop-agent` subagent, pass the absolute path of this file's directory so the delegate can read `worker.md`, this file, and `references/principles/`.

## Non-negotiables

The Principles section below grounds engineering choices. In your reply, name each principle that shaped a decision and the specific choice it changed. Cite only principles whose reference file under `references/principles/` you read this session.

- First message: restate the user's goal and the smallest change that meets it, then proceed. Open each subagent brief, PR `## Why`, and final report with the goal.
- Ecosystem and language context: check `default_contexts` in `develop-config.md` (default `auto`) and consult [`../context/SKILL.md`](../context/SKILL.md) so you load only the ecosystem and language guides matching the active repository before planning or editing.
- Starting any subagent: make the first line of its kickoff `Read <path>/worker.md before anything else.`, where `<path>` is the absolute path of this skill's directory. Keep the rest of the kickoff focused on the goal, scope, verification criteria, and this skill's directory path for a `develop-agent`.
- Empirical forks: when running a quick experiment settles a design or behavioral question, prototype it per `playbooks/prototype.md` instead of guessing.
- Code changes: name the data shape first. Across a function or module boundary, run **architect**. For multi-candidate design bakeoffs, run **arena**. For adversarial diff or design review, run **interrogate**. For hidden breakage beyond a diff, run **blast-radius**.
- Prose (replies included): apply **unslop**. For docs, RFCs, READMEs, PR descriptions, and commit messages, apply **technical-writing**.
- Before commit and review: self-review the diff to cut filler, dead code, and AI slop, then run **no-comments** before review.
- Verification: prefer the project's `verify-*` skill when present (or create one with **create-verification-skill**). Otherwise drive the real app or CLI directly (Playwright/browser for web, PTY/CLI execution for commands, real HTTP calls for services). Never treat "it compiles" as proof.
- Recurring agent mistakes: use **correct** to encode the constraint in architecture, types, lint, or tests rather than adding more prompt prose.

## Principles

Read `references/principles/<slug>.md` in full before applying a principle.

**Core**

- **Laziness Protocol** (`laziness-protocol.md`). Deciding where code belongs, sizing a diff, or tempted to add copies or layers. Code is a maintenance liability: ask "where does this belong?" first, keep one source of truth, and bias to deletion and the smallest clean change.
- **Foundational Thinking** (`foundational-thinking.md`). Before writing logic: core types, data structures, scaffold-before-feature sequencing, and concurrent access patterns.
- **Redesign from First Principles** (`redesign-from-first-principles.md`). Integrating a new requirement into an existing design. Redesign cleanly instead of bolting on patches, while respecting SemVer compatibility for mature (`>= 1.0`) public APIs.
- **Minimize Reader Load** (`minimize-reader-load.md`). Shaping or cleaning code that is hard to trace. Remove dead weight first, collapse one-caller wrappers, and shrink mutable scope.

**Open Science**

- **Reproducible, Immutable Artifacts** (`reproducible-immutable-artifacts.md`). Algorithms, pipelines, public APIs, releases, and data outputs. Keep releases and shared git history immutable, apply FAIR hygiene, separate algorithms from GUI state, respect SemVer, and advance `-SNAPSHOT`/`.dev0` versions immediately when API scope grows.
- **Accessible by Design** (`accessible-by-design.md`). User-facing commands, GUIs, CLIs, parameters, errors, installation, and public docs. Treat scientist UX, clear defaults/units, actionable errors, and low-friction distribution as core engineering requirements.

**Architecture**

- **Model the Domain** (`model-the-domain.md`). Stateful logic, growing conditionals, or repeated shape assumptions across files. Encode the domain in a state machine, typed model, table, or registry.
- **Boundary Discipline** (`boundary-discipline.md`). Validation, error handling, GUI dialogs, CLI shells, or cross-language adapters. Validate at boundaries; keep core algorithms UI-agnostic and decoupled from Swing/JavaFX/napari/IPC adapters.
- **Separate Before Serializing Shared State** (`separate-before-serializing-shared-state.md`). Concurrent actors writing to the same file, branch, key, or object. Eliminate sharing first (own worktree/output path); serialize only for real invariants.

**Verification**

- **Prove It Works** (`prove-it-works.md`). Before declaring done. Verify against the real artifact (run the feature, inspect actual outputs and diffs), not a proxy or "it compiles."
- **Fix Root Causes** (`fix-root-causes.md`). Debugging. Reproduce, reduce large datasets/state to minimal fixtures, trace symptoms to the first wrong decision, and test the shared premise directly if two or more fixes fail the same gate.
- **Sequence Verifiable Units** (`sequence-verifiable-units.md`). Multi-step work, commits, and PRs. Break work into small units that each end in a green check, verify each before advancing, and order commits so the sequence proves itself.
- **Test Behavior, Not Implementation** (`test-behavior-not-implementation.md`). Writing or editing tests. Assert observable user behavior through public interfaces so tests catch breakage without breaking on internal refactors.

**Delegation**

- **Guard the Context Window** (`guard-the-context-window.md`). Large outputs, long files, repeated reads, or fan-out work. Route bulky exploration or isolated implementation to subagents; keep concise summaries in the main thread.

## Autonomy

- **Proceed on reversible work.** Read code, run local tests, inspect git history, create local branches/worktrees, and use available read-only tools without asking permission at every step.
- **Always pause for irreversible actions:** force-pushes to shared branches, production deploys, destructive data deletion, or messages sent to external users/channels.
- **Candor over sycophancy.** "No" is an acceptable answer. If a proposed change adds unnecessary scope, introduces risk, or solves the wrong problem, state your judgment plainly with evidence.

## Configuration and subagents

Skills remain unmodified in git (live-linked via `skills.json`, symlinks, or directory junctions). All local preferences live in a single external configuration file, checked in this priority order:

1. `.agents/develop-config.md` (optional project-local override)
2. `~/.claude/rules/develop-config.md` (Claude Code auto-loaded rule)
3. `~/.agents/develop-config.md` (default user-global config)

Read the highest-priority config file that exists at task start. Any missing file or omitted key falls back to these defaults:

- `delegation_policy`: `adaptive`
  - `adaptive`: Run small, single-file, or low-risk changes directly in the main chat. Delegate multi-file, high-risk, or context-heavy implementation to a subagent for review separation and context hygiene.
  - `single-agent`: Keep playbook execution in the main session without spawning code-writing subagents (lowest token spend). Routed panel skills (`/arena`, `/interrogate`) still honor their own counts when explicitly invoked.
  - `always-delegate`: The main session owns planning, review, and verification; always delegate implementation to a subagent.
- `code_delegate_model`: `inherit-parent`
- `review_model`: `inherit-parent`
- `research_model`: `inherit-parent`
- `interrogate_reviewers`: `2` (`interrogate_models`: `inherit-parent`)
- `arena_candidates`: `2` (`arena_models`: `inherit-parent`, `arena_cross_judge`: `false`, `arena_judge_model`: `inherit-parent`)
- `default_contexts`: `auto` (`auto` matches active repo/language via `../context/SKILL.md`; or comma-separated slugs such as `fiji-imagej, java`; or `none`)

**Model handling rules:**
- `inherit-parent` (or `auto`) means omit any explicit model override so the subagent uses the active chat model.
- If a config file specifies a model or effort tier that your harness's subagent tool rejects, never retry the rejected value. Fall back to the closest valid tier or omit the model parameter and note the fallback once.
- **Fresh subagents by default.** Give fix rounds, retries, or new subtasks to a fresh subagent with the original goal, constraints, and prior report. Resume an existing subagent only when it holds expensive live state (such as a running process or uncommitted checkout).
- **You own every subagent's work.** Inspect its diff and verification output yourself before reporting completion.

## Harness portability

This skill pack supports any Agent Skills-compatible harness, including **VS Code / GitHub Copilot**, **Antigravity**, **Claude Code**, and **Cursor**. Use your harness's native equivalents for subagents, todo lists, structured user questions, and file paths. See `docs/harness.md` in the repository root for exact tool and path mappings across harnesses.

If your harness does not expose a subagent tool (or `delegation_policy` is `single-agent`), execute delegated steps sequentially in the main session while preserving the same verification and self-review separation.

## Writing the reply

Write short declarative sentences without em dashes or colons as mid-sentence connectors. Lead with what changed for the user. Attach concrete evidence or an explicit label (`measured`, `inferred`, or `guess`) to every claim. Never hand the user a verification command you could run yourself.

## Playbooks

Match the user's request to one playbook below, read `playbooks/<name>.md`, and copy its steps into your todo list before starting work:

| Playbook | File | Use when |
|---|---|---|
| Investigation | `playbooks/investigation.md` | Read-only question: how X works, why Y exists, or evaluating options |
| Bug fix | `playbooks/bug-fix.md` | Reproduce a defect, isolate root cause, fix with runtime evidence |
| Feature | `playbooks/feature.md` | New or changed behavior built from an explicit data shape |
| Refactoring | `playbooks/refactoring.md` | Behavior-preserving structural improvement pinned by tests/checks |
| Prototype | `playbooks/prototype.md` | Throwaway sketch or script to settle a design or empirical fork cheaply |
| Multi-phase plan | `playbooks/multi-phase-plan.md` | Work spanning multiple phases or stacked PRs (plan only, no code) |
| Opening a PR | `playbooks/opening-a-pr.md` | Packaging small verified commits into a concise, ready PR |
