---
name: develop
description: "Structured engineering workflow for investigations, bug fixes, features, refactoring, prototypes, multi-phase plans, and pull requests. Provide your goal, how to verify success (pass/fail check), and any constraints; if details are missing, the agent asks before editing. Use for /develop."
disable-model-invocation: true
---

# Develop

Sibling skills live at `../<name>/SKILL.md` relative to this file. When delegating implementation to a subagent, pass the absolute path of this file's directory so the delegate can read `worker.md`, this file, `references/config-and-subagents.md`, and `references/principles/`.

## Before starting

Check that you have enough information before editing any files:

- **No task provided (bare `/develop`):** Ask the user for their goal, how to verify success (a concrete pass/fail check), and any constraints. Briefly list the seven supported workflows (investigation, bug fix, feature, refactoring, prototype, multi-phase plan, and opening a PR) so newcomers know what `/develop` covers, and link the quick-reference sheet and system overview from `references/config-and-subagents.md` Section 8 when the user asks what commands exist or which skill fits their task.
- **Read-only question (Investigation):** Proceed directly without asking for a pass/fail check.
- **Code-changing task with unclear scope or missing success criteria:** Propose a concise goal and concrete pass/fail check in two or three lines, and ask the user to confirm or adjust before editing code.
- **Concrete task with clear criteria or a reproducible bug:** Restate the goal, the pass/fail check, and the smallest change that meets it in your first message, then proceed.

## Non-negotiables

The Principles section below grounds engineering choices. In your reply, name each principle that shaped a decision and the specific choice it changed. Cite only principles whose reference file under `references/principles/` you read this session.

- First message: restate the user's goal, pass/fail check, and the smallest change that meets it (or pause per `Before starting` if critical criteria are missing). Open each subagent brief, PR `## Why`, and final report with the goal.
- Ecosystem and language context: resolve `default_contexts` per `references/config-and-subagents.md` (default `auto`) and consult [`../context/SKILL.md`](../context/SKILL.md) so you load only the configured or repo-matching ecosystem and language guides before planning or editing.
- Starting any subagent: follow `references/config-and-subagents.md` Section 4. Make the first line of every subagent kickoff `Read <path>/worker.md before anything else.`, where `<path>` is the absolute path of this skill's directory. Keep the rest of the kickoff focused on the goal, scope, verification criteria, and this skill's directory path for implementation delegates.
- Empirical forks: when a quick experiment settles a design or behavioral question, prototype it per `playbooks/prototype.md` instead of guessing.
- Code changes: name the data shape first. Across a public/shared interface or module boundary, run **architect**. For side-by-side competing designs, run **arena** (respecting `delegation_policy`). For adversarial diff or design review, run **interrogate** (respecting `delegation_policy`). For hidden breakage beyond a diff, run **blast-radius**.
- Prose (replies included): apply **unslop**. For docs, RFCs, READMEs, PR descriptions, and commit messages, apply **technical-writing**.
- Before commit and review: self-review the diff to cut filler, dead code, and common AI writing patterns, then run **audit-comments**.
- Verification: prefer the project's `verify-*` skill when present (or offer to create one with **create-verification-skill**). Otherwise drive the real app, CLI, API, or library directly. Never treat "it compiles" as proof.
- Recurring agent mistakes: use **correct** to encode the constraint in architecture, types, lint, or tests rather than adding more prompt prose.

## Principles

Read `references/principles/<slug>.md` in full before applying a principle.

**Core**

- **Laziness Protocol** (`laziness-protocol.md`). Deciding where code belongs, sizing a diff, or tempted to add copies or layers. Code is a maintenance liability: ask "where does this belong?" first, keep one source of truth, and bias to deletion and the smallest clean change.
- **Foundational Thinking** (`foundational-thinking.md`). Before writing logic: core types, data structures, scaffold-before-feature sequencing, and concurrent access patterns.
- **Redesign from First Principles** (`redesign-from-first-principles.md`). Integrating a new requirement into an existing design. Redesign cleanly instead of bolting on patches, while respecting Semantic Versioning (SemVer) compatibility for mature (`>= 1.0`) public APIs.
- **Minimize Reader Load** (`minimize-reader-load.md`). Shaping or cleaning code that is hard to trace. Remove dead weight first, collapse one-caller wrappers, shrink mutable scope, and honor least surprise in function contracts.

**Open Science**

- **Reproducible, Immutable Artifacts** (`reproducible-immutable-artifacts.md`). Algorithms, pipelines, public APIs, releases, and data outputs. Keep releases and shared git history immutable, apply FAIR (Findable, Accessible, Interoperable, Reusable) hygiene, separate algorithms from GUI state, respect SemVer, and advance `-SNAPSHOT` or `.dev0` versions immediately when API scope grows.
- **Accessible by Design** (`accessible-by-design.md`). User-facing commands, GUIs, CLIs, parameters, public APIs, errors, installation, and public docs. Apply the principle of least surprise, treat user experience, clear defaults and units, actionable errors, explicit confirmation for risky side effects, and low-friction distribution as core engineering requirements.

**Architecture**

- **Model the Domain** (`model-the-domain.md`). Stateful logic, growing conditionals, or repeated shape assumptions across files. Encode the domain in a state machine, typed model, table, or registry.
- **Boundary Discipline** (`boundary-discipline.md`). Validation, error handling, GUI dialogs, CLI shells, or cross-language adapters. Validate at boundaries, fail loudly rather than silently coercing or falling back, and keep core algorithms UI-agnostic and decoupled from Swing, JavaFX, napari, or IPC adapters.
- **Separate Before Serializing Shared State** (`separate-before-serializing-shared-state.md`). Concurrent actors writing to the same file, branch, key, or object. Eliminate sharing first (own worktree or output path); serialize only for real invariants.

**Verification**

- **Prove It Works** (`prove-it-works.md`). Before declaring done. Verify against the real artifact (run the feature, inspect actual outputs and diffs), not a proxy or "it compiles."
- **Fix Root Causes** (`fix-root-causes.md`). Debugging. Reproduce, reduce large datasets or state to minimal fixtures, trace symptoms to the first wrong decision, and test the shared premise directly if two or more fixes fail the same gate.
- **Sequence Verifiable Units** (`sequence-verifiable-units.md`). Multi-step work, commits, and PRs. Break work into small units that each end in a green check, verify each before advancing, and order commits so the sequence proves itself.
- **Test Behavior, Not Implementation** (`test-behavior-not-implementation.md`). Writing or editing tests. Assert observable user behavior through public interfaces so tests catch breakage without breaking on internal refactors.

**Delegation**

- **Guard the Context Window** (`guard-the-context-window.md`). Large outputs, long files, repeated reads, or fan-out work. Route bulky exploration or isolated implementation to subagents; keep concise summaries in the main thread.

## Autonomy

- **Proceed on reversible work.** Read code, run local tests, inspect git history, create local branches or worktrees, and use read-only tools without asking permission at every step.
- **Always pause for irreversible or external actions:** force-pushes to shared branches, pushing branches or opening pull requests (unless explicitly requested), production deploys, destructive data deletion, or messages sent to external users or channels.
- **Candor over sycophancy.** "No" is an acceptable answer. If a proposed change adds unnecessary scope, introduces risk, or solves the wrong problem, state your judgment plainly with evidence.

## Configuration, subagents, and portability

Read [`references/config-and-subagents.md`](references/config-and-subagents.md) for the single authoritative specification of:

- External config lookup and key-level override merging (`~/.agents/develop-config.md` or `~/.claude/rules/develop-config.md` base, overlaid by optional `<target-repo>/.agents/develop-config.md`)
- `delegation_policy` (`adaptive`, `single-agent`, `always-delegate`), `parallel_subagents`, effort-tier models (`high_effort_model`, `medium_effort_model`, `low_effort_model`), `default_contexts`, and legacy v1.0-1.2 key fallbacks
- Supported subagent model values, the `worker.md` kickoff rule, and the deprecated-model fallback protocol
- Tool and capability mappings across coding assistants (Antigravity, VS Code / GitHub Copilot, Claude Code, Cursor, and other Agent Skills assistants) and graceful single-agent fallbacks
- Developer aides and command discovery paths (`docs/overview.md`, `docs/quick-reference.md`, and `docs/handouts/agent-skills-handout.pdf`) for bare invocations or skill confusion

**You own every subagent's work.** Inspect its diff and verification output yourself before reporting completion.

## Writing the reply

Write short declarative sentences without em dashes or colons as mid-sentence connectors. Lead with what changed for the user. Attach concrete evidence (commands run, observed outputs, or file paths) to verified claims, and mark any unverified inference or assumption explicitly. Never hand the user a verification command you could run yourself.

## Playbooks

Match the user's request to one playbook below, read `playbooks/<name>.md`, and copy its steps into your todo list before starting work:

| Playbook | File | Use when |
|---|---|---|
| Investigation | [`playbooks/investigation.md`](playbooks/investigation.md) | Read-only question: how X works, why Y exists, or evaluating options |
| Bug fix | [`playbooks/bug-fix.md`](playbooks/bug-fix.md) | Reproduce a defect, isolate root cause, fix with runtime evidence |
| Feature | [`playbooks/feature.md`](playbooks/feature.md) | New or changed behavior built from an explicit data shape |
| Refactoring | [`playbooks/refactoring.md`](playbooks/refactoring.md) | Behavior-preserving structural improvement pinned by tests or checks |
| Prototype | [`playbooks/prototype.md`](playbooks/prototype.md) | Throwaway sketch or script to settle a design or empirical fork cheaply |
| Multi-phase plan | [`playbooks/multi-phase-plan.md`](playbooks/multi-phase-plan.md) | Work spanning multiple phases or stacked PRs (plan only, no code) |
| Opening a PR | [`playbooks/opening-a-pr.md`](playbooks/opening-a-pr.md) | Packaging small verified commits into a concise, ready PR |
