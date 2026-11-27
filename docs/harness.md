# Cross-Harness Reference

This kit follows the [Agent Skills](https://agentskills.io) `SKILL.md` standard and avoids vendor-specific runtime features so it works across any compatible harness. Primary mappings below cover **VS Code / GitHub Copilot**, **Antigravity**, **Claude Code**, and **Cursor** (not an exhaustive list — other compatible harnesses generally use `.agents/skills/` and `~/.agents/skills/`).

## 1. Discovery paths

| Asset | VS Code / GitHub Copilot | Antigravity | Claude Code | Cursor |
|---|---|---|---|---|
| **Project skills** | `.agents/skills/<name>/SKILL.md` or `.github/skills/<name>/SKILL.md` | `.agents/skills.json` (recommended for live-linked clones) or `.agents/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` | `.cursor/skills/<name>/SKILL.md` or `.agents/skills/<name>/SKILL.md` |
| **User-global skills** | `~/.copilot/skills/<name>/SKILL.md` or `~/.agents/skills/<name>/SKILL.md` | `~/.gemini/config/skills.json` (recommended — explicit forward-slash path to `<repo_path>/skills`) or `~/.gemini/config/skills/<name>/SKILL.md` (real dirs only on Windows; junctions are skipped) | `~/.claude/skills/<name>/SKILL.md` | `~/.cursor/skills/<name>/SKILL.md` |
| **Config file (checked in order)** | 1. `.agents/develop-config.md`<br>2. `~/.agents/develop-config.md` | 1. `.agents/develop-config.md`<br>2. `~/.agents/develop-config.md` | 1. `.agents/develop-config.md`<br>2. `~/.claude/rules/develop-config.md` (auto-loaded)<br>3. `~/.agents/develop-config.md` | 1. `.agents/develop-config.md`<br>2. `~/.agents/develop-config.md` |
| **Custom agent files** | `.github/agents/*.agent.md` or `~/.copilot/agents/*.agent.md` | Dynamic via `define_subagent` / `invoke_subagent` (no static agent file needed) | `.claude/agents/*.md` or `~/.claude/agents/*.md` | `.cursor/agents/*.md` or `~/.cursor/agents/*.md` |
| **Always-on repo instructions** | `AGENTS.md` or `.github/copilot-instructions.md` | `AGENTS.md` or `GEMINI.md` | `CLAUDE.md` (and `~/.claude/rules/*.md`) | `AGENTS.md` or `.cursor/rules/*.mdc` |

## 2. Tool and capability mappings

Skills describe actions generically (spawn a subagent, track a todo list, ask the user a structured question). Map each action to your active harness:

| Action in skills | VS Code / GitHub Copilot | Antigravity | Claude Code | Cursor |
|---|---|---|---|---|
| **Spawn general delegate (`develop-agent`)** | Subagent / custom agent (`develop-agent` if installed, else general subagent with kickoff pointing to `develop/worker.md` and `develop/SKILL.md`) | `invoke_subagent` (`TypeName: "self"`, passing kickoff pointing to `develop/worker.md` and `develop/SKILL.md`) | `Agent` (`subagent_type: "develop-agent"` if linked in `agents/`, else `"general-purpose"` with kickoff prompt) | `Task` (`subagent_type: "develop-agent"` if linked in `agents/`, else `generalPurpose` with kickoff prompt) |
| **Spawn read-only researcher (`/how`, `/no-comments`)** | Read-only subagent or `comment-auditor` custom agent; else pass `references/comment-auditor.md` verbatim | `invoke_subagent` (`TypeName: "research"` for read-only exploration, or `"self"` with strict read-only prompt) | `Agent` (`subagent_type: "Explore"` or `"comment-auditor"` with explicit "do not edit files" instruction) | `Task` (`subagent_type: "comment-auditor"` or `generalPurpose` with `readonly: true`) |
| **Isolated parallel work (`/arena`, `/interrogate`)** | Separate git worktrees (`git worktree add`) or `/tmp` output dirs per worker | `invoke_subagent` with `Workspace: "share"` or `"branch"` (or explicit git worktrees) | `Agent` with `isolation: "worktree"` (or explicit git worktrees) | Separate git worktrees (or cloud subagents if enabled by the user) |
| **Todo / step tracking** | Native task/todo list if available; otherwise keep a concise checklist in replies | `update_steps` / `update_focus` | `TodoWrite` (or concise checklist in replies in non-interactive mode) | Native todo list tool |
| **Structured user questions** | Native question prompt or numbered options in chat | `ask_question` | `AskUserQuestion` (plain numbered options in `-p` mode) | `AskQuestion` |
| **Invoke sibling skill** | Read `../<name>/SKILL.md` directly and follow it | Read `../<name>/SKILL.md` directly and follow it | Read `../<name>/SKILL.md` directly (most skills set `disable-model-invocation: true`, so read directly rather than relying on the `Skill` tool) | Read `../<name>/SKILL.md` directly and follow it |
| **Auto-discover context guides (`context`)** | `skills/context/SKILL.md` omits `disable-model-invocation` so Copilot discovers matching guides automatically (or via `/context` / `default_contexts`) | Progressive discovery loads `skills/context/SKILL.md` on matching repo/language (or via `/context` / `default_contexts`) | Model-invocable `context` skill auto-triggers on matching repo/language (or via `/context` / `default_contexts`) | Model-invocable `context` skill auto-triggers on matching repo/language (or via `/context` / `default_contexts`) |

## 3. Subagent effort tiers, model syntax, and deprecation fallback

`develop-config.md` configures subagent models using three effort tiers that default to `inherit`. When a tier is set to `inherit` (or legacy alias `inherit-parent` / `auto`), omit any explicit model override so the subagent uses the active chat model.

### Effort-tier mapping

| Tier key | Workload | Skills and tasks |
|---|---|---|
| `high_effort_model` | Complex design comparisons, adversarial bug hunting, judging competing solutions | `/arena` (candidates and optional cross-judge), `/interrogate` (adversarial reviewers) |
| `medium_effort_model` | Scoped code implementation from a plan, structured diff and comment review | `/develop` (`develop-agent` in `feature`, `bug-fix`, `refactoring`), `/no-comments` (`comment-auditor`) |
| `low_effort_model` | Fast read-only codebase walkthroughs and feature-file scanning | `/how` (architecture walkthrough), `/maintain-verification-skill` (source-wave readers) |

Parallel multi-agent skills (`/arena` and `/interrogate`) read `parallel_subagents` (default `2`) for fan-out count. `/arena` requires at least `2` candidates to compare designs, so if `parallel_subagents` is `1`, `/arena` runs `2` candidates and notes that override once. Set optional `arena_cross_judge: true` in `develop-config.md` if you always want an extra judge subagent (on `high_effort_model`) during `/arena`.

### Supported subagent model values by coding assistant

Always inspect your active subagent tool schema before asking the user for model values. Never ask for or store subscription plan names. Pass only values accepted by the active assistant:

| Assistant | What the subagent tool accepts | Examples |
|---|---|---|
| **Antigravity** | Fixed built-in model classes on `invoke_subagent`'s `Model` parameter: `inherit`, `pro`, `flash`, `flash_lite`. These are model sizes, not subscription plans. `invoke_subagent` rejects individual model names such as `Gemini 4 Neon`. | `high_effort_model: pro`, `medium_effort_model: flash`, `low_effort_model: flash_lite` |
| **Claude Code** | Model aliases (`opus`, `sonnet`, `haiku`) or explicit model IDs, plus optional reasoning effort (`low`, `medium`, `high`, `xhigh`) written as `<model> <effort>`. Omit for `inherit`. | `high_effort_model: opus high`, `medium_effort_model: sonnet`, `low_effort_model: haiku` |
| **VS Code / GitHub Copilot** | Active chat model (`inherit`) or exact model identifiers exposed by the user's Copilot plan or custom `.agent.md` `model:` header. | `high_effort_model: Claude Opus 4.6`, `medium_effort_model: Claude Sonnet 4.6`, `low_effort_model: inherit` |
| **Cursor** | Active chat model (`inherit`) or exact model identifiers accepted by Cursor's `Task` tool. | `high_effort_model: claude-sonnet-4-5`, `medium_effort_model: inherit`, `low_effort_model: fast` |
| **Other Agent Skills assistants** | Inspect the active subagent tool's model parameter; default to `inherit` if no model selector is exposed. | `high_effort_model: inherit` |

In assistants that accept concrete model names, `high_effort_model` also accepts a comma-separated list (for example, `opus high, sonnet high`). Parallel high-effort skills assign listed models round-robin across subagents, and single-subagent callers use the first entry.

### Legacy v1.0-1.2 config key fallbacks

If an existing `develop-config.md` omits the current keys and still contains v1.0-1.2 keys, read the legacy keys as fallbacks so existing setups keep working:

| Current key | Legacy fallback key(s) |
|---|---|
| `parallel_subagents` | `interrogate_reviewers` (for `/interrogate`), `arena_candidates` (for `/arena`) |
| `high_effort_model` | `interrogate_models` (for `/interrogate`), `arena_models` and `arena_judge_model` (for `/arena`) |
| `medium_effort_model` | `code_delegate_model` (for `/develop`), `review_model` (for `/no-comments`) |
| `low_effort_model` | `research_model` (for `/how`, `/maintain-verification-skill`) |
| `inherit` | `inherit-parent`, `auto` |

### Deprecated or unsupported model fallback protocol

Models are deprecated and renamed over time, and users may switch coding assistants while sharing one `develop-config.md`. Whenever a subagent tool rejects a configured model value:

1. **Never retry** the rejected value during the same session.
2. **Fall back immediately to `inherit`** (omit the model override) so the subagent runs on the active chat model and the current task completes without losing work.
3. **Report a deprecation notice once** in your reply containing:
   - The active `develop-config.md` file path
   - The offending config key and rejected value
   - Confirmation that the run fell back to `inherit`
   - The currently valid model values accepted by this coding assistant's subagent tool
   - An offer to update `develop-config.md` and re-run Suite 3 Check 5 of [docs/validation.md](validation.md)
4. **Do not silently edit `develop-config.md`** during an unrelated task. Wait for user confirmation before modifying their configuration file.

## 4. Session transcripts for `/reflect`

When running `/reflect`, stay strictly inside the active workspace's session history:

- **Antigravity:** Current conversation transcript at `<appDataDir>/brain/<conversation-id>/.system_generated/logs/transcript.jsonl` (start with the compact file).
- **Claude Code:** `~/.claude/projects/<workspace-slug>/<session>.jsonl` (where `<workspace-slug>` replaces non-alphanumeric characters with `-`).
- **Cursor:** The workspace's `agent-transcripts/` directory named in the system prompt (never other workspaces').
- **VS Code / GitHub Copilot & other harnesses:** Use the active conversation context directly (or exported chat session if supplied by the user).

## 5. Graceful fallbacks

- **No subagent tool available (or `delegation_policy: single-agent`):** Execute delegated steps sequentially in the main session. Preserve review separation by re-reading the full `git diff` critically before verifying.
- **No image-generation tool (`/teach`):** Use clean incremental Mermaid or ASCII diagrams instead.
- **No project `verify-*` skill yet:** Drive the real app with local tools (test suite, CLI command, Playwright/browser automation, or HTTP requests), and offer `/create-verification-skill` when the project would benefit from repeatable verification.
- **Windows without Developer Mode or Admin rights:** On **Antigravity**, register `<repo_path>/skills` in `~/.gemini/config/skills.json` (or `<target>/.agents/skills.json`) using an explicit forward-slash absolute path (do not use `~/` on Windows or NTFS directory junctions, which Antigravity's directory walker skips). On other harnesses (Copilot, Claude Code, Cursor), use directory junctions (`New-Item -ItemType Junction` or `mklink /J`) instead of symbolic links for skill folders.
