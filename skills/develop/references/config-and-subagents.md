# Runtime configuration, subagents, and assistant mappings

Single runtime reference shared by `/develop` and sibling skills. Because this file lives inside `skills/develop/references/`, every skill resolves it at `../develop/references/config-and-subagents.md` even when installed into another repository or copied statically.

In this kit, **coding assistant** and **harness** both refer to the Agent Skills runtime (Antigravity, VS Code / GitHub Copilot, Claude Code, Cursor, or another compatible assistant).

## 1. Configuration lookup and override merging

Skills stay unmodified in git. Local preferences live in `develop-config.md`, loaded as follows:

1. **User-global base:** Read `~/.agents/develop-config.md` if it exists. If it does not exist, fall back to `~/.claude/rules/develop-config.md` (Claude Code's auto-loaded rule). Always edit `~/.agents/develop-config.md` as the primary user-global file (and on Windows, re-copy it to `~/.claude/rules/develop-config.md` when Claude Code uses a static copy).
2. **Project-local overlay:** If `<target-repo>/.agents/develop-config.md` exists, overlay any keys it defines on top of the user-global base. If no user-global file exists, read the project-local file directly.
3. **Built-in defaults:** Any missing file or omitted key falls back to the defaults below.

| Key | Default | Allowed values and behavior |
|---|---|---|
| `delegation_policy` | `adaptive` | `adaptive` (small local edits in main chat; multi-file, high-risk, or exploration-heavy work to a subagent), `single-agent` (no helper subagents in standard flows; ask before escalating to multi-agent skills), `always-delegate` (main chat plans, reviews, and verifies; implementation goes to a subagent) |
| `parallel_subagents` | `2` | Integer >= `1`. Fan-out count for `/interrogate` and `/arena`, and concurrency batch size for `/maintain-verification-skill`. `/arena` requires at least `2` candidates (if set to `1`, run `2` and note the override once). |
| `high_effort_model` | `inherit` | Model for `/arena` candidates and optional judge, and `/interrogate` adversaries. Accepts a comma-separated list on assistants that allow concrete model names (assigned round-robin across parallel subagents; single-subagent callers use the first entry, while an optional `/arena` judge picks an alternate entry or legacy `arena_judge_model` when available). |
| `medium_effort_model` | `inherit` | Model for `/develop` implementation delegates and `/audit-comments` (`comment-auditor`). |
| `low_effort_model` | `inherit` | Model for `/how` codebase walkthroughs and `/maintain-verification-skill` source readers. |
| `default_contexts` | `auto` | `auto` (match active repo and language via `../context/SKILL.md`), `none` (manual `/context <slug>` only), or comma-separated slugs such as `fiji-imagej, java` (always load those exact guides automatically). |
| `arena_cross_judge` | `false` | Optional boolean (`true` or `false`). When `true`, `/arena` spawns an extra read-only judge subagent using `high_effort_model`. |

**Project-local safety rule:** Keep `<target-repo>/.agents/develop-config.md` untracked or in `.gitignore` whenever it contains machine-local paths (`repo_path`) or personal preferences. Only commit a project-local `.agents/develop-config.md` if it contains team-shared overrides (for example, `default_contexts: tme-quant, python`).

**Multi-assistant note:** `~/.agents/develop-config.md` is shared by every coding assistant you install into on this machine. If you use more than one coding assistant (for example, Antigravity and Claude Code), keep all three model tiers set to `inherit` so assistant-specific model values (such as `pro` versus `opus`) never collide.

### Minimal `develop-config.md` schema

```markdown
# develop configuration
# Read by /develop, /context, /create-context-guide, /reflect, and subagent skills.
# Keep skills/ immutable; edit this file to change models, parallelism, contexts, or delegation.

## Installation
harness: <antigravity | copilot | claude-code | cursor | other>
repo_path: <absolute path to the local uw-loci/agent-skills clone>
install_scope: <user-global | project-local>
install_method: <skills-json | symlink | junction | copy>

## Subagent Delegation & Parallelism
delegation_policy: <adaptive | single-agent | always-delegate>
parallel_subagents: <1-3, default 2>

## Subagent Models (by effort tier; use `inherit` to reuse the active chat model)
high_effort_model: <inherit | assistant-accepted model value>
medium_effort_model: <inherit | assistant-accepted model value>
low_effort_model: <inherit | assistant-accepted model value>

## Context Guides
default_contexts: <auto | none | comma-separated slugs>
```

## 2. Legacy v1.0-1.2 config key fallbacks

If an existing `develop-config.md` omits a current key and defines a legacy key from v1.0-1.2, read the legacy key as a fallback:

| Current key or value | Legacy fallback keys or values |
|---|---|
| `parallel_subagents` | `interrogate_reviewers` (for `/interrogate`), `arena_candidates` (for `/arena`) |
| `high_effort_model` | `interrogate_models` (for `/interrogate`), `arena_models` and `arena_judge_model` (for `/arena`) |
| `medium_effort_model` | `code_delegate_model` (for `/develop`), `review_model` (for `/audit-comments`) |
| `low_effort_model` | `research_model` (for `/how`, `/maintain-verification-skill`) |
| `inherit` | `inherit-parent`, `auto` |

When a tier resolves to `inherit` (or legacy `inherit-parent` or `auto`), omit any explicit model override so the subagent uses the active chat model.

## 3. Supported subagent model values by coding assistant

Always inspect your active subagent tool schema before asking the user for model values. Never ask for or store subscription plan names. Pass only values accepted by the active coding assistant:

| Coding assistant | What the subagent tool accepts | Examples |
|---|---|---|
| **Antigravity** | Fixed built-in model classes on `invoke_subagent`'s `Model` parameter: `inherit`, `pro`, `flash`, `flash_lite`. These are model sizes, not subscription plans. `invoke_subagent` rejects individual model names such as `gemini-2.5-pro`. | `high_effort_model: pro`, `medium_effort_model: flash`, `low_effort_model: flash_lite` |
| **Claude Code** | Model aliases (`opus`, `sonnet`, `haiku`) or explicit model IDs. If an optional reasoning effort (`low`, `medium`, `high`, `xhigh`, `max`) is appended as `<model> <effort>`, pass `<model>` and `<effort>` as separate tool parameters when supported, or omit `<effort>` if the active `Agent` tool accepts only `model`. Omit both for `inherit`. | `high_effort_model: opus`, `medium_effort_model: sonnet`, `low_effort_model: haiku` |
| **VS Code / GitHub Copilot** | Active chat model (`inherit`) or exact model identifiers exposed by the user's Copilot plan or custom `.agent.md` `model:` header. | `high_effort_model: Claude Opus 4.6`, `medium_effort_model: Claude Sonnet 4.6`, `low_effort_model: inherit` |
| **Cursor** | Active chat model (`inherit`) or exact model identifiers accepted by Cursor's `Task` tool. | `high_effort_model: claude-sonnet-4-5`, `medium_effort_model: inherit`, `low_effort_model: fast` |
| **Other Agent Skills assistants** | Inspect the active subagent tool's model parameter; default to `inherit` if no model selector is exposed. | `high_effort_model: inherit` |

## 4. Subagent kickoff and deprecated-model fallback protocol

- **Mandatory kickoff first line:** Start every spawned subagent prompt (implementation delegates, `/arena` candidates and judge, `/interrogate` adversaries, `/how` readers, `/audit-comments` auditor, and `/maintain-verification-skill` source readers) with:
  `Read <develop-dir>/worker.md before anything else.`
  where `<develop-dir>` is the absolute path of the installed `skills/develop` directory.
- **Fresh subagents by default:** Send fix rounds, retries, and new subtasks to a fresh subagent with the original goal, constraints, and prior report. Reuse an existing subagent only when it holds live state such as a running process or uncommitted checkout.
- **Deprecated or unsupported model fallback:** Whenever a subagent tool rejects a configured model value because it was deprecated, renamed, or is unsupported by the active coding assistant:
  1. Never retry the rejected value during the same session.
  2. Fall back immediately to `inherit` (omit the model override) so the task finishes cleanly without losing work.
  3. Report a one-time deprecation notice in your reply containing:
     - The active `develop-config.md` path
     - The config key and rejected value
     - Confirmation that the run fell back to `inherit`
     - The valid model values accepted by the active coding assistant's subagent tool
     - An offer to update `develop-config.md` and re-run Suite 3 Check 5 of `<repo_path>/docs/validation.md` (or run a lightweight `worker.md` subagent check directly if installed as a static copy without a local clone)
  4. Do not edit `develop-config.md` without explicit user confirmation.

## 5. Tool and capability mappings across coding assistants

| Action in skills | VS Code / GitHub Copilot | Antigravity | Claude Code | Cursor |
|---|---|---|---|---|
| **Spawn implementation delegate** | General subagent with `worker.md` and `develop/SKILL.md` kickoff | `invoke_subagent` (`TypeName: "self"` with `worker.md` and `develop/SKILL.md` kickoff) | `Agent` (`subagent_type: "general-purpose"` with `worker.md` and `develop/SKILL.md` kickoff) | `Task` (`subagent_type: "generalPurpose"` with `worker.md` and `develop/SKILL.md` kickoff) |
| **Spawn read-only researcher (`/how`, `/audit-comments`, `/maintain-verification-skill`)** | Read-only subagent (pass `references/comment-auditor.md` verbatim for `/audit-comments`) | `invoke_subagent` (`TypeName: "research"` for read-only lookups, or `"self"` with strict read-only instructions) | `Agent` (`subagent_type: "Explore"` with explicit "do not edit files" instruction) | `Task` (`subagent_type: "generalPurpose"` with `readonly: true`) |
| **Isolated parallel work (`/arena`, `/interrogate`)** | Separate git worktrees (`git worktree add`) or OS temp directories (`$env:TEMP` in PowerShell / `%TEMP%` in cmd on Windows; `/tmp` on macOS and Linux) | `invoke_subagent` with `Workspace: "share"` (new isolated workspace sharing the `.git` directory, like `git worktree`) or `"branch"` (isolated clone), or separate git worktrees / OS temp directories | `Agent` with `isolation: "worktree"` (or separate git worktrees / OS temp directories) | Separate git worktrees (or OS temp directories) |
| **Todo / step tracking** | Native task list if available; otherwise a concise checklist in replies | `update_steps` and `update_focus` | `TodoWrite` (or concise checklist in non-interactive mode) | Native todo list tool |
| **Structured user questions** | Native question prompt (multi-select when available) or numbered options in chat | `ask_question` (`is_multi_select: true` for checklists) | `AskUserQuestion` (`multiSelect: true`, up to 4 options per question; plain numbered options in `-p` mode) | `AskQuestion` (multi-select when available, or numbered options) |
| **Invoke sibling skill** | Read `../<name>/SKILL.md` directly and follow it | Read `../<name>/SKILL.md` directly and follow it | Read `../<name>/SKILL.md` directly (19 of 20 skills set `disable-model-invocation: true`, so read directly instead of using the `Skill` tool) | Read `../<name>/SKILL.md` directly and follow it |
| **Auto-discover and configure context guides (`/context`)** | `skills/context/SKILL.md` omits `disable-model-invocation` so matching guides load automatically (or via `/context`, `/context <slug>`, `/context configure`) | Progressive discovery loads `skills/context/SKILL.md` on matching repos and languages | Model-invocable `context` skill auto-triggers on matching repos and languages | Model-invocable `context` skill auto-triggers on matching repos and languages |

## 6. Session transcript locations for `/reflect`

Stay strictly inside the active workspace's session history. Never read transcripts from unrelated projects:

- **Antigravity:** Current conversation transcript at `<appDataDir>/brain/<conversation-id>/.system_generated/logs/transcript.jsonl` (start with the compact file).
- **Claude Code:** `~/.claude/projects/<workspace-slug>/<session>.jsonl` (where `<workspace-slug>` replaces non-alphanumeric characters with `-`).
- **Cursor:** The workspace's `agent-transcripts/` directory named in the system prompt.
- **VS Code / GitHub Copilot and other assistants:** Use the active conversation context directly (or an exported transcript supplied by the user).

## 7. Graceful fallbacks

- **No subagent tool available, or `delegation_policy: single-agent`:** Execute delegated steps sequentially in the main session, and re-read the full `git diff` critically before verifying. Under `single-agent`, do not autonomously escalate to multi-agent `/arena` or `/interrogate` fan-out without asking the user first and noting the token multiplier.
- **No image-generation tool (`/teach`):** Draw incremental Mermaid or ASCII diagrams instead.
- **No project `verify-*` skill yet:** Drive the real app, CLI, library, or endpoint with local tools, and offer `/create-verification-skill` when repeatable verification would help.
