# Cross-Harness Reference

This kit targets three harnesses: **VS Code / GitHub Copilot**, **Antigravity**, and **Claude Code**. Every skill in `skills/` follows the [Agent Skills](https://agentskills.io) `SKILL.md` standard and avoids vendor-specific runtime features.

## 1. Discovery paths

| Asset | VS Code / GitHub Copilot | Antigravity | Claude Code |
|---|---|---|---|
| **Project skills** | `.agents/skills/<name>/SKILL.md` or `.github/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` |
| **User-global skills** | `~/.copilot/skills/<name>/SKILL.md` or `~/.agents/skills/<name>/SKILL.md` | `~/.gemini/config/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` |
| **Config file (checked in order)** | 1. `.agents/develop-config.md`<br>2. `~/.agents/develop-config.md` | 1. `.agents/develop-config.md`<br>2. `~/.agents/develop-config.md` | 1. `.agents/develop-config.md`<br>2. `~/.claude/rules/develop-config.md` (auto-loaded)<br>3. `~/.agents/develop-config.md` |
| **Custom agent files** | `.github/agents/*.agent.md` or `~/.copilot/agents/*.agent.md` | Dynamic via `define_subagent` / `invoke_subagent` (no static agent file needed) | `.claude/agents/*.md` or `~/.claude/agents/*.md` |
| **Always-on repo instructions** | `AGENTS.md` or `.github/copilot-instructions.md` | `AGENTS.md` or `GEMINI.md` | `CLAUDE.md` (and `~/.claude/rules/*.md`) |

## 2. Tool and capability mappings

Skills describe actions generically (spawn a subagent, track a todo list, ask the user a structured question). Map each action to your active harness:

| Action in skills | VS Code / GitHub Copilot | Antigravity | Claude Code |
|---|---|---|---|
| **Spawn general delegate (`develop-agent`)** | Subagent / custom agent (`develop-agent` if installed, else general subagent with kickoff prompt pointing to `develop/worker.md` and `develop/SKILL.md`) | `invoke_subagent` (`TypeName: "self"`, passing kickoff pointing to `develop/worker.md` and `develop/SKILL.md`) | `Agent` (`subagent_type: "develop-agent"` if linked in `agents/`, else `"general-purpose"` with kickoff prompt) |
| **Spawn read-only researcher (`/how`, `/no-comments`)** | Read-only subagent or `comment-auditor` custom agent; else pass `references/comment-auditor.md` verbatim | `invoke_subagent` (`TypeName: "research"` for read-only exploration, or `"self"` with strict read-only prompt) | `Agent` (`subagent_type: "Explore"` or `"comment-auditor"` with explicit "do not edit files" instruction) |
| **Isolated parallel work (`/arena`, `/interrogate`)** | Separate git worktrees (`git worktree add`) or `/tmp` output dirs per worker | `invoke_subagent` with `Workspace: "share"` or `"branch"` (or explicit git worktrees) | `Agent` with `isolation: "worktree"` (or explicit git worktrees) |
| **Todo / step tracking** | Native task/todo list if available; otherwise keep a concise checklist in replies | `update_steps` / `update_focus` | `TodoWrite` (or concise checklist in replies in non-interactive mode) |
| **Structured user questions** | Native question prompt or numbered options in chat | `ask_question` | `AskUserQuestion` (plain numbered options in `-p` mode) |
| **Invoke sibling skill** | Read `../<name>/SKILL.md` directly and follow it | Read `../<name>/SKILL.md` directly and follow it | Read `../<name>/SKILL.md` directly (most skills set `disable-model-invocation: true`, so read directly rather than relying on the `Skill` tool) |
| **Auto-discover context guides (`context`)** | `skills/context/SKILL.md` omits `disable-model-invocation` so Copilot discovers matching guides automatically (or via `/context` / `default_contexts`) | Progressive discovery loads `skills/context/SKILL.md` on matching repo/language (or via `/context` / `default_contexts`) | Model-invocable `context` skill auto-triggers on matching repo/language (or via `/context` / `default_contexts`) |

## 3. Model and reasoning-tier mappings

`develop-config.md` defaults every role to `inherit-parent`, which means **omit any explicit model override** so subagents inherit the active session's model.

When a user configures explicit models or tiers in `develop-config.md`, pass only values accepted by the active harness:

| Harness | Supported subagent model syntax | Examples |
|---|---|---|
| **Antigravity** | `Model` parameter on `invoke_subagent`: `inherit`, `flash_lite`, `flash`, `pro` | `code_delegate_model: inherit`, `research_model: flash`, `arena_models: pro, flash` |
| **Claude Code** | `model` (`opus`, `sonnet`, `haiku`) + optional `effort` (`low`, `medium`, `high`, `xhigh`) written as `<model> <effort>` | `code_delegate_model: sonnet high`, `review_model: opus high`, `research_model: haiku` |
| **VS Code / GitHub Copilot** | Active chat model (`inherit-parent`) or model identifiers exposed by the user's Copilot plan / custom `.agent.md` `model:` header | `code_delegate_model: inherit-parent` |

**Fallback rule:** If a harness rejects a configured model value, never retry the rejected slug. Fall back to the closest valid tier or omit the model parameter (`inherit-parent`), continue the task, and report the fallback once.

## 4. Session transcripts for `/reflect`

When running `/reflect`, stay strictly inside the active workspace's session history:

- **Antigravity:** Current conversation transcript at `<appDataDir>/brain/<conversation-id>/.system_generated/logs/transcript.jsonl` (start with the compact file).
- **Claude Code:** `~/.claude/projects/<workspace-slug>/<session>.jsonl` (where `<workspace-slug>` replaces non-alphanumeric characters with `-`).
- **VS Code / GitHub Copilot:** Use the active conversation context directly (or exported chat session if supplied by the user).

## 5. Graceful fallbacks

- **No subagent tool available (or `delegation_policy: single-agent`):** Execute delegated steps sequentially in the main session. Preserve review separation by re-reading the full `git diff` critically before verifying.
- **No image-generation tool (`/teach`):** Use clean incremental Mermaid or ASCII diagrams instead.
- **No project `verify-*` skill yet:** Drive the real app with local tools (test suite, CLI command, Playwright/browser automation, or HTTP requests), and offer `/create-verification-skill` when the project would benefit from repeatable verification.
- **Windows without Developer Mode or Admin rights:** Use directory junctions (`New-Item -ItemType Junction` or `mklink /J`) instead of symbolic links for skill folders.
