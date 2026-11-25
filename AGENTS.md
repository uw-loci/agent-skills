# Agent Installation & Configuration Guide

This repository (`uw-loci/agent-skills`) contains a curated, harness-portable set of **20 Agent Skills** centered on `/develop`, **7 playbooks**, **12 engineering principles**, **5 development context guides** (under `skills/context/references/`), and **2 subagent definitions** (`develop-agent` and `comment-auditor`).

## Core rule: keep skills immutable

**Never edit or regex-replace `SKILL.md` files during installation.** Keep all files in `skills/` untouched so symlinks or directory junctions stay clean and `git pull` updates apply without conflicts. Store all user choices in a single external configuration file (`develop-config.md`).

---

## Step 1: Prompt the user for installation choices

Before creating links or writing configuration, ask the user for the choices below. Use your harness's structured question tool when available; otherwise present concise numbered choices. Propose the defaults first so the user can accept quickly.

1. **Target harness(es):** Which harness(es) should be configured?
   - `VS Code / GitHub Copilot`
   - `Antigravity`
   - `Claude Code`
   - Any combination of the above
2. **Install scope:**
   - **User-global (Recommended):** Available across all repositories on this machine.
   - **Project-local:** Installed into a specific target repository path (ask for the target path).
3. **Link method:**
   - **Symlink / Junction (Recommended):** Live-linked to this local clone so `git pull` updates everything automatically. On Windows, prefer directory junctions (`mklink /J` or `New-Item -ItemType Junction`), which work without Administrator privileges or Developer Mode.
   - **Copy:** Static copy fallback if links are restricted in the user's environment.
4. **Delegation policy (token usage control):**
   - `adaptive` **(Recommended default):** Single-agent for small/single-file tasks; delegate multi-file, high-risk, or context-heavy tasks to `develop-agent`.
   - `single-agent`: Lowest token usage; run playbooks directly in the main session without spawning code-writing subagents.
   - `always-delegate`: Main chat owns design, review, and verification; always delegate implementation to a subagent.
5. **Models per role:**
   - Inspect which models or subagent tiers are available in the active harness (see [docs/harness.md](docs/harness.md)).
   - Offer `inherit-parent` **(Recommended default)** for `code_delegate_model`, `review_model`, and `research_model`, or let the user assign specific harness-valid models/tiers (for example, `pro` / `flash` in Antigravity, `opus high` / `sonnet high` in Claude Code, or Copilot-available models).
6. **Orchestrator panel sizes and models:**
   - **`/interrogate` (adversarial diff review):** Number of parallel reviewers (`interrogate_reviewers`, default `2`, typical range `1`-`3`) and model list (`interrogate_models`, default `inherit-parent`).
   - **`/arena` (multi-candidate design bakeoff):** Number of parallel candidates (`arena_candidates`, default `2`, typical range `2`-`3`), `arena_models` (default `inherit-parent`), and whether to spawn an extra cross-judge (`arena_cross_judge`, default `false`; plus `arena_judge_model`, default `inherit-parent`).
7. **Default development context guides (`default_contexts`):**
   - `auto` **(Recommended default):** Automatically load only matching UW-LOCI ecosystem/language guides (`fiji-imagej`, `tme-quant`, `qupath`, `java`, `python`) based on the active repository via `skills/context/SKILL.md`.
   - Explicit comma-separated slugs (for example, `fiji-imagej, java` or `tme-quant, python`) — especially useful for project-local `.agents/develop-config.md` files.
   - `none`: Load context guides only when explicitly invoked via `/context <slug>`.
   - *(Tip: mention `/create-context-guide` if the user works in an additional multi-repo stack not yet covered.)*

---

## Step 2: Write `develop-config.md`

Write the user's answers to the external configuration file (never inside `skills/`):

- **User-global default:** `~/.agents/develop-config.md`
  - **Claude Code users:** Also symlink (or copy if symlinks are unavailable) `~/.claude/rules/develop-config.md` to `~/.agents/develop-config.md` so Claude Code auto-loads it into every new session.
- **Project-local override:** `<target-repo>/.agents/develop-config.md`

Use this exact schema (preserve all keys; delete any optional override later to revert to defaults):

```markdown
# develop configuration
# Read by /develop and orchestrator skills (/arena, /interrogate, /no-comments, /how, /reflect).
# Keep skills/ immutable; edit this file to change models, panel sizes, or delegation behavior.

## Installation
harness: <copilot | antigravity | claude-code | comma-separated list>
repo_path: <absolute path to this uw-loci/agent-skills clone>
install_scope: <user-global | project-local>
install_method: <symlink | junction | copy>

## Delegation & Token Control
delegation_policy: <adaptive | single-agent | always-delegate>

## Models (use `inherit-parent` to stay on the active chat model)
code_delegate_model: <inherit-parent | harness-valid model/tier>
review_model: <inherit-parent | harness-valid model/tier>
research_model: <inherit-parent | harness-valid model/tier>

## Orchestrator Panels (controls fan-out count and token multiplier)
interrogate_reviewers: <1-3, default 2>
interrogate_models: <inherit-parent | comma-separated list>

arena_candidates: <2-3, default 2>
arena_models: <inherit-parent | comma-separated list>
arena_cross_judge: <false | true>
arena_judge_model: <inherit-parent | harness-valid model/tier>

## Context Guides (progressive-disclosure repo maps & language conventions)
default_contexts: <auto | none | comma-separated slugs, e.g. fiji-imagej, java>
```

---

## Step 3: Link (or copy) skills and agents per harness

Link every directory under `skills/` (all 20 skills) into the destination directory for each selected harness. See [docs/harness.md](docs/harness.md) for complete harness details.

| Harness | User-global skills dir | Project-local skills dir | Agent definitions |
|---|---|---|---|
| **VS Code / GitHub Copilot** | `~/.copilot/skills/` (or `~/.agents/skills/`) | `<target>/.agents/skills/` (or `.github/skills/`) | Optional: copy/link `agents/develop-agent.md` and `agents/comment-auditor.md` as `.agent.md` files in `~/.copilot/agents/` or `<target>/.github/agents/` |
| **Antigravity** | `~/.gemini/config/skills/` | `<target>/.agents/skills/` | Not required separately (skills reference `worker.md` and `references/comment-auditor.md` directly) |
| **Claude Code** | `~/.claude/skills/` | `<target>/.claude/skills/` | Link `agents/develop-agent.md` and `agents/comment-auditor.md` into `~/.claude/agents/` (or `<target>/.claude/agents/`) |

> **Shared project-local tip:** Both VS Code / GitHub Copilot and Antigravity discover `<target>/.agents/skills/` automatically. A single install into `<target>/.agents/skills/` covers both harnesses; only Claude Code needs `<target>/.claude/skills/` linked in addition.

### Reference linking commands

Replace `<REPO>` with this repository's absolute path and `<DEST>` with the target skills directory above. Always check for existing non-link directories before replacing them, and ask before overwriting user-authored skills.

- **Windows (PowerShell — directory junctions, no Admin required):**
  ```powershell
  New-Item -ItemType Directory -Force -Path "<DEST>" | Out-Null
  Get-ChildItem -Directory "<REPO>\skills" | ForEach-Object {
      $target = Join-Path "<DEST>" $_.Name
      if (Test-Path $target) { Remove-Item $target -Force }
      New-Item -ItemType Junction -Path $target -Target $_.FullName | Out-Null
  }
  ```
- **macOS / Linux (POSIX shell — symlinks):**
  ```bash
  mkdir -p "<DEST>"
  for d in "<REPO>"/skills/*/; do
      name="$(basename "$d")"
      ln -sfn "${d%/}" "<DEST>/$name"
  done
  ```
- **Copy fallback:** Copy each directory under `<REPO>/skills/` into `<DEST>/` and record `install_method: copy` in `develop-config.md`.

---

## Step 4: Run post-install validation

Immediately after installation (and whenever skills are updated or reconfigured), read and execute **[docs/validation.md](docs/validation.md)**.

Report the full PASS / WARN / FAIL table to the user before declaring installation complete. Remind the user to open a **new chat session** (or reload the IDE window) so the harness refreshes its discovered skill catalog.

---

## Reconfiguring later

To change models, panel counts, `delegation_policy`, or `default_contexts` later, edit `develop-config.md` directly (or ask an agent to update it) and re-run Suite 2 of [docs/validation.md](docs/validation.md). No skill files need to be edited or relinked.
