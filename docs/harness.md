# Cross-assistant installation and discovery reference

This kit follows the [Agent Skills](https://agentskills.io) `SKILL.md` standard and avoids vendor-specific runtime features so it works across any compatible coding assistant (**VS Code / GitHub Copilot**, **Antigravity**, **Claude Code**, **Cursor**, and other compatible tools, which generally discover `.agents/skills/` and `~/.agents/skills/`).

In configuration files and command references, the key `harness` refers to the active coding assistant.

## 1. Discovery paths

| Asset | VS Code / GitHub Copilot | Antigravity | Claude Code | Cursor |
|---|---|---|---|---|
| **Project skills** | `.agents/skills/<name>/SKILL.md` or `.github/skills/<name>/SKILL.md` | `.agents/skills.json` (recommended for live-linked clones) or `.agents/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` | `.cursor/skills/<name>/SKILL.md` or `.agents/skills/<name>/SKILL.md` |
| **User-global skills** | `~/.copilot/skills/<name>/SKILL.md` or `~/.agents/skills/<name>/SKILL.md` | `~/.gemini/config/skills.json` (recommended: explicit forward-slash path to `<repo_path>/skills`) or `~/.gemini/config/skills/<name>/SKILL.md` (real directories only on Windows; junctions are skipped) | `~/.claude/skills/<name>/SKILL.md` | `~/.cursor/skills/<name>/SKILL.md` |
| **Config file (base + overlay)** | Base `~/.agents/develop-config.md`, overlaid by `.agents/develop-config.md` | Base `~/.agents/develop-config.md`, overlaid by `.agents/develop-config.md` | Base `~/.agents/develop-config.md` (linked or copied at `~/.claude/rules/develop-config.md` for auto-loading), overlaid by `.agents/develop-config.md` | Base `~/.agents/develop-config.md`, overlaid by `.agents/develop-config.md` |
| **Custom agent files (optional)** | `.github/agents/*.agent.md` or `~/.copilot/agents/*.agent.md` (not shipped; see Section 3) | Dynamic via `define_subagent` / `invoke_subagent` (no static agent file needed) | `.claude/agents/*.md` or `~/.claude/agents/*.md` (not shipped; see Section 3) | `.cursor/agents/*.md` or `~/.cursor/agents/*.md` (not shipped; see Section 3) |
| **Always-on repo instructions** | `AGENTS.md` or `.github/copilot-instructions.md` | `AGENTS.md` or `GEMINI.md` | `CLAUDE.md` (and `~/.claude/rules/*.md`) | `AGENTS.md` or `.cursor/rules/*.mdc` |

## 2. Windows installation notes (no Developer Mode or Admin required)

- **Antigravity on Windows:** Register `<repo_path>/skills` in `~/.gemini/config/skills.json` (user-global) or `<target>/.agents/skills.json` (project-local) using an explicit forward-slash absolute path (for example, `C:/Users/<user>/code/uw-loci/agent-skills/skills`). Do not use `~/` in `skills.json` on Windows because it is not expanded, and do not create NTFS directory junctions inside `~/.gemini/config/skills/` because Antigravity's Windows directory scanner skips junction reparse points.
- **Copilot, Claude Code, and Cursor on Windows:** Use NTFS directory junctions (`New-Item -ItemType Junction` or `mklink /J`) instead of symbolic links for skill folders. Junctions require no administrator rights or Developer Mode.

## 3. Optional custom agent files

This kit deliberately ships no separate `agents/` directory so subagent instructions stay in one place without duplicated copies. Every skill works out of the box across all supported coding assistants by spawning your assistant's built-in subagent tool with [`skills/develop/worker.md`](../skills/develop/worker.md) or [`skills/audit-comments/references/comment-auditor.md`](../skills/audit-comments/references/comment-auditor.md).

If you use **Claude Code**, **VS Code / GitHub Copilot**, or **Cursor** and specifically want named custom agents in your assistant's UI (for example, to invoke `@comment-auditor` directly or enforce assistant-level read-only tool allowlists), create thin local wrapper files in your assistant's `agents/` directory from the table above. Point each wrapper to read `<repo_path>/skills/develop/worker.md` or `<repo_path>/skills/audit-comments/references/comment-auditor.md` rather than duplicating their prompt bodies so updates stay in sync after `git pull`.

## 4. Runtime config, model values, tool mappings, and fallbacks

All runtime configuration rules live in one shared file inside the installed skill tree so every skill can read it from any repository:

- **[`skills/develop/references/config-and-subagents.md`](../skills/develop/references/config-and-subagents.md)** covers:
  - Configuration priority, key-level override merging, multi-assistant safety, and project-local `.gitignore` guidance
  - Effort tiers (`high_effort_model`, `medium_effort_model`, `low_effort_model`), `parallel_subagents`, and legacy v1.0-1.2 key fallbacks
  - Supported subagent model values for Antigravity, Claude Code, VS Code / GitHub Copilot, and Cursor
  - Subagent `worker.md` kickoff rules and the deprecated-model fallback protocol
  - Tool mappings across coding assistants, `/reflect` session transcript locations, and graceful fallbacks
