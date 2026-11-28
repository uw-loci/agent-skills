# Agent installation and configuration guide

This repository (`uw-loci/agent-skills`) contains a curated, cross-assistant set of **20 Agent Skills** centered on `/develop`, **7 playbooks**, **14 engineering principles**, and **5 development context guides** (under `skills/context/references/`).

## Core rule: keep skills immutable

**Never edit or regex-replace `SKILL.md` files during installation.** Keep all files in `skills/` untouched so `skills.json` manifests, symlinks, or directory junctions stay clean and `git pull` updates apply without conflicts. Store all user choices in a single external configuration file (`develop-config.md`).

---

## Step 1: Confirm environment and installation choices

Detect the active coding assistant and operating system before asking questions. Walk through the seven decisions below with the user.

Follow these interview rules:

- **One decision per question.** Never bundle unrelated settings, such as parallel subagent counts and model selection, into the same question.
- **Explain the impact in plain language.** Each question must state what the user is choosing, why it matters, and how it affects behavior or token usage. Do not assume the user knows internal skill names, playbook names, or repository jargon.
- **Give concrete, actionable options.** Never ask the user to guess valid values or enter subscription plan names.
- **Keep the flow brisk.** Use your assistant's structured question UI when available, or concise numbered options in chat. You may present 3 to 4 independent single-decision questions in one structured prompt, or split the interview into two short rounds, while keeping recommended defaults clear.

### 1. Confirm the active coding assistant

- **Decision:** Confirm which coding assistant you are installing these skills into.
- **Why it matters:** Each coding assistant reads skills from a different location and provides its own subagent tool.
- **How to ask:** Name the detected assistant (for example, Antigravity, VS Code / GitHub Copilot, Claude Code, Cursor, or another [Agent Skills](https://agentskills.io)-compatible assistant) and OS, and ask the user to confirm. If the assistant is not listed in Step 3, confirm its skills directory (typically `~/.agents/skills/` for user-global or `<target>/.agents/skills/` for project-local). Only configure an extra assistant if the user explicitly asks.

### 2. Choose install scope

- **Decision:** Should these skills be available in every repository on this machine, or only inside one repository?
- **Why it matters:** A global install works everywhere with one setup. A project-local install limits skills and settings to one repository.
- **Options:**
  - **User-global (Recommended):** Available across all repositories on this machine.
  - **Project-local:** Installed into one specific repository (ask for the target repository path).

### 3. Choose how skills stay up to date

- **Decision:** Should your coding assistant point directly to this local git clone, or use a copied snapshot?
- **Why it matters:** Live-linking keeps every skill up to date whenever you run `git pull`, with no reinstall. Copying creates a static snapshot that you must recopy after updates.
- **Options:**
  - **Live-linked (Recommended):** Stay synced with this git clone automatically. *(Agent note: use the live mechanism for the confirmed assistant from Step 3, such as `skills.json` for Antigravity, Windows directory junctions for other assistants, or POSIX symlinks on macOS and Linux. Keep filesystem mechanics out of the user question unless linking fails.)*
  - **Static copy:** Copy skill files into the assistant's folder. Choose this only if manifests, symlinks, or junctions are restricted in your environment.

> **No subagent tool?** If the confirmed coding assistant cannot spawn subagents at all, skip Questions 4, 5, and 6, note that subagent features will run sequentially in the main chat, and record `delegation_policy: single-agent`, `parallel_subagents: 2`, and `inherit` for all three model tiers.

### 4. Choose when to delegate work to helper subagents (`delegation_policy`)

- **Decision:** Should workflows hand larger implementation or codebase-exploration steps to a helper subagent, or do all steps in the main chat?
- **Why it matters:** Delegating bulky edits and codebase scans keeps your main chat focused on planning and review and limits context bloat, at the cost of extra tokens.
- **Options:**
  - **`adaptive` (Recommended):** Do small, single-file edits directly in the main chat. Hand off larger multi-file, risky, or exploration-heavy tasks to a helper subagent.
  - **`single-agent`:** Keep standard workflows in the main chat without spawning helper subagents (lowest token spend).
  - **`always-delegate`:** Keep the main chat for design, review, and verification. Always hand implementation edits to a helper subagent (strictest review separation, higher token spend).

### 5. Choose parallel subagent count (`parallel_subagents`)

- **Decision:** When a multi-agent workflow runs parallel subagents (such as side-by-side design comparisons or adversarial bug reviews), how many subagents should it start?
- **Why it matters:** More parallel subagents catch more edge cases and explore more design options, but each extra subagent multiplies token usage for that run. *(If the user chose `single-agent` in Question 4, note briefly that this count applies only when they explicitly run a multi-agent workflow.)*
- **Options:**
  - **`2` (Recommended):** Balances independent perspectives and token cost.
  - **`3`:** Broader coverage at roughly 3x the token cost on multi-agent runs.
  - **`1`:** Lowest token cost (runs a single reviewer; side-by-side comparison workflows still require at least `2` candidates).

### 6. Choose subagent models by effort tier

- **Decision:** Should subagents reuse your active chat model (`inherit`), or use specific models chosen by task effort?
- **Why it matters:** Using `inherit` follows whichever model you select in chat and needs zero upkeep when models change. Choosing models by effort lets light read-only lookups use faster, cheaper models while heavy design and review tasks use a stronger model. *(If the user chose `single-agent` in Question 4, note briefly that these settings apply only when they explicitly run a multi-agent workflow.)*
- **Mandatory pre-check before asking:** Inspect your active coding assistant's subagent tool schema or available model list (see [skills/develop/references/config-and-subagents.md](skills/develop/references/config-and-subagents.md)) before asking:
  - **If the subagent tool has no model parameter**, tell the user that subagents always inherit the active chat model, set all three tiers to `inherit`, and skip asking this question.
  - **If the subagent tool accepts concrete model names or aliases** (for example, Claude Code, VS Code / GitHub Copilot, or Cursor), list the accepted model identifiers and ask for concrete model names (never subscription plan names).
  - **If the subagent tool restricts subagents to fixed built-in model classes** (for example, Antigravity's `invoke_subagent` accepts only `inherit`, `pro`, `flash`, and `flash_lite`, and rejects individual model names), state that restriction plainly. Clarify that those values are built-in model sizes, not subscription plans. Use `pro` for the largest model class, `flash` for a faster lighter class, and `flash_lite` for the lightest class.
- **How to link effort tiers to model values:** When presenting this question (especially if placing notes above a structured question UI), introduce the effort tiers before (or explicitly linked to) the assistant's supported model values so the user understands why both are shown. Explain in plain language that this skill kit groups subagent tasks into three effort tiers, and the user can leave all three on `inherit` or assign one of the assistant's accepted models or classes to each tier:
  - **High effort (`high_effort_model`):** Complex design comparisons, adversarial bug hunting, and judging competing solutions.
  - **Medium effort (`medium_effort_model`):** Scoped code implementation from a plan and structured diff or comment reviews.
  - **Low effort (`low_effort_model`):** Fast read-only codebase walkthroughs and file scanning.
- **Options:**
  - **`inherit` for all tiers (Recommended):** Every subagent reuses your active chat model.
  - **Custom models by effort tier:** Provide three values from the assistant's supported list, one each for High, Medium, and Low effort (for example, in Claude Code: `opus`, `sonnet`, `haiku`; in Antigravity: `pro`, `flash`, `flash_lite`). If you plan to use more than one coding assistant sharing `~/.agents/develop-config.md`, keep all three tiers on `inherit` so assistant-specific model values do not collide.

### 7. Choose automatic project and language guides (`default_contexts`)

- **Decision:** Should UW-LOCI ecosystem and language guides load automatically when you open a matching repository?
- **Why it matters:** Auto-loading only the guides that match your active repo gives the assistant accurate local build commands and conventions without adding unrelated stacks to your context window.
- **Guide catalog:** Read the live **Ecosystem guides** and **Language guides** tables in [skills/context/SKILL.md](skills/context/SKILL.md) instead of hardcoding guide names. Briefly summarize what guides are currently available in one sentence, and do not ask the user to type guide slugs from memory.
- **Options:**
  - **`auto` (Recommended):** Detect the active repository and load only matching guides automatically.
  - **Choose specific guides now:** Open a follow-up checklist of every currently available ecosystem and language guide so you can select the exact ones to load.
  - **`none`:** Load guides only when you request `/context <slug>` manually.
- **If the user selects "Choose specific guides now":** Immediately run the interactive guide picker in [skills/context/SKILL.md](skills/context/SKILL.md) (Step 3 of `Configuring default guides`) before writing `develop-config.md`, using native multi-select checkboxes when available or a numbered checklist in chat.
- *(Tip: mention `/context configure` to change active guides interactively later, and `/create-context-guide` if the user works in another multi-repo stack not covered yet.)*

---

## Step 2: Write `develop-config.md`

Write the user's answers to the external configuration file (never inside `skills/`):

- **User-global default:** `~/.agents/develop-config.md`
  - **Claude Code users:** Also symlink (or copy if symlinks are unavailable) `~/.claude/rules/develop-config.md` to `~/.agents/develop-config.md` so Claude Code auto-loads it into every new session.
- **Project-local install or override:** `<target-repo>/.agents/develop-config.md`
  - **Git hygiene warning:** When installing project-locally (writing machine-local `repo_path` or personal model choices), remind the user to add `.agents/develop-config.md` to `.gitignore` or `.git/info/exclude` so personal paths are not committed. Project-local files also support **key-level overlays** on top of `~/.agents/develop-config.md`, so teams can safely commit a minimal `.agents/develop-config.md` containing only shared settings such as `default_contexts: tme-quant, python`.

Use this exact schema (preserve all keys for a full install; delete any optional override later to revert to defaults):

```markdown
# develop configuration
# Read by /develop, /context, /create-context-guide, /reflect, and subagent skills.
# Keep skills/ immutable; edit this file to change models, parallelism, contexts, or delegation.

## Installation
harness: <antigravity | copilot | claude-code | cursor | other>
repo_path: <absolute path to this uw-loci/agent-skills clone>
install_scope: <user-global | project-local>
install_method: <skills-json | symlink | junction | copy>

## Subagent Delegation & Parallelism
delegation_policy: <adaptive | single-agent | always-delegate>
parallel_subagents: <1-3, default 2>

## Subagent Models (by effort tier; use `inherit` to reuse the active chat model)
high_effort_model: <inherit | assistant-accepted model value>
medium_effort_model: <inherit | assistant-accepted model value>
low_effort_model: <inherit | assistant-accepted model value>

## Context Guides (progressive-disclosure repo maps and language conventions)
default_contexts: <auto | none | comma-separated slugs, for example fiji-imagej, java>
```

Optional advanced overrides (omitted by default, documented in [skills/develop/references/config-and-subagents.md](skills/develop/references/config-and-subagents.md)):

- `arena_cross_judge: true` adds a separate read-only judge subagent (using `high_effort_model`) during `/arena` runs.
- In assistants that accept concrete model names, `high_effort_model` also accepts a comma-separated list (for example, `opus, sonnet` in Claude Code) to spread parallel high-effort runs across multiple models.
- Existing v1.0-1.2 configs that still use legacy per-role keys (`code_delegate_model`, `review_model`, `research_model`, `interrogate_reviewers`, `interrogate_models`, `arena_candidates`, `arena_models`, `arena_judge_model`, `inherit-parent`, or `auto`) continue to work via fallback. Suite 2 of [docs/validation.md](docs/validation.md) flags them for cleanup.

---

## Step 3: Register, link (or copy) skills

Register or link every directory under `skills/` (all 20 skills) for the confirmed coding assistant. Common destinations are listed below (see [docs/harness.md](docs/harness.md) for full details and notes on optional user-created custom agent wrappers):

| Coding assistant | User-global skills config or dir | Project-local skills config or dir |
|---|---|---|
| **Antigravity** | `~/.gemini/config/skills.json` (register `<REPO>/skills`; use `~/.gemini/config/skills/` only for static copies, because Windows junctions are skipped) | `<target>/.agents/skills.json` (or `<target>/.agents/skills/` for copies or POSIX symlinks) |
| **VS Code / GitHub Copilot** | `~/.copilot/skills/` (or `~/.agents/skills/`) | `<target>/.agents/skills/` (or `.github/skills/`) |
| **Claude Code** | `~/.claude/skills/` | `<target>/.claude/skills/` |
| **Cursor** | `~/.cursor/skills/` | `<target>/.cursor/skills/` (or `.agents/skills/`) |
| **Other Agent Skills assistant** | `~/.agents/skills/` (or assistant-configured global path) | `<target>/.agents/skills/` |

> **Shared project-local tip:** Antigravity, VS Code / GitHub Copilot, Cursor, and most Agent Skills-compatible assistants discover `<target>/.agents/skills/` automatically. Antigravity also reads `<target>/.agents/skills.json`.

### Reference installation commands

Replace `<REPO>`, `<target>`, and `<DEST>` with explicit **absolute paths**. Always check for existing non-link directories before replacing them, and ask before overwriting user-authored skills. For project-local live-linked installs (`skills.json`, symlinks, or junctions), also remind the user to add `.agents/skills.json` or `.agents/skills/` (or `.claude/skills/`, `.cursor/skills/`) to `.gitignore` or `.git/info/exclude` so machine-local absolute paths are not committed to a shared repository.

- **Antigravity (all OSes, native `skills.json` manifest, recommended):**
  Register `<REPO>/skills` in `~/.gemini/config/skills.json` (user-global) or `<target>/.agents/skills.json` (project-local) and record `install_method: skills-json` in `develop-config.md`.
  - **Windows note:** Always write an **explicit absolute path with forward slashes** (for example `C:/Users/<user>/code/uw-loci/agent-skills/skills`). Do **not** use `~/` in `skills.json` on Windows (it is not expanded), and do **not** create NTFS directory junctions inside `~/.gemini/config/skills/` (Antigravity's Windows directory scanner skips junction reparse points).
  - If `skills.json` already exists, merge the entry into `"entries"` rather than overwriting existing user entries:
    ```json
    {
      "entries": [
        {
          "path": "<ABSOLUTE_FORWARD_SLASH_PATH_TO_REPO>/skills"
        }
      ]
    }
    ```
  - **PowerShell merge helper (Windows):**
    ```powershell
    $manifest = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath("$HOME\.gemini\config\skills.json") # or "<target>\.agents\skills.json"
    $skillsPath = (("<REPO>".TrimEnd('\', '/')) + '/skills') -replace '[\\/]+', '/'
    New-Item -ItemType Directory -Force -Path (Split-Path $manifest) | Out-Null
    $raw = if (Test-Path $manifest) { Get-Content $manifest -Raw -Encoding UTF8 } else { '' }
    $cfg = if ($raw -and $raw.Trim()) { $raw | ConvertFrom-Json } else { $null }
    if (-not $cfg) { $cfg = [PSCustomObject]@{ entries = @() } }
    if (-not ($cfg.PSObject.Properties.Name -contains 'entries') -or -not $cfg.entries) {
        $cfg | Add-Member -NotePropertyName entries -NotePropertyValue @() -Force
    }
    $exists = $cfg.entries | Where-Object { (($_.path -replace '[\\/]+', '/').TrimEnd('/')) -ieq $skillsPath }
    if (-not $exists) {
        $cfg.entries = @($cfg.entries) + [PSCustomObject]@{ path = $skillsPath }
    }
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($manifest, ($cfg | ConvertTo-Json -Depth 5), $utf8NoBom)
    ```
- **Windows for non-Antigravity assistants (PowerShell directory junctions, no Admin required):**
  *(Do not use for Antigravity; use `skills.json` above instead.)*
  ```powershell
  $dest = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath("<DEST>")
  New-Item -ItemType Directory -Force -Path $dest | Out-Null
  Get-ChildItem -Directory "<REPO>\skills" | ForEach-Object {
      $target = Join-Path $dest $_.Name
      $item = Get-Item -LiteralPath $target -Force -ErrorAction SilentlyContinue
      if ($item) {
          if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
              [System.IO.Directory]::Delete($target)
          } else {
              throw "Refusing to overwrite non-link directory: $target"
          }
      }
      New-Item -ItemType Junction -Path $target -Target $_.FullName | Out-Null
  }
  ```
- **macOS / Linux (POSIX shell symlinks):**
  ```bash
  mkdir -p "<DEST>"
  for d in "<REPO>"/skills/*/; do
      [ -d "$d" ] || continue
      name="$(basename "$d")"
      target="<DEST>/$name"
      if [ -e "$target" ] && [ ! -L "$target" ]; then
          echo "Refusing to overwrite non-link directory: $target" >&2
          exit 1
      fi
      ln -sfn "${d%/}" "$target"
  done
  ```
- **Copy fallback:** Copy each directory under `<REPO>/skills/` into `<DEST>/` (for Antigravity, real directories inside `~/.gemini/config/skills/` or `<target>/.agents/skills/`) and record `install_method: copy` in `develop-config.md`.
- **Claude Code auto-loaded config rule (user-global only):**
  - **macOS / Linux:**
    ```bash
    mkdir -p "$HOME/.claude/rules"
    ln -sfn "$HOME/.agents/develop-config.md" "$HOME/.claude/rules/develop-config.md"
    ```
  - **Windows:** Copy `~/.agents/develop-config.md` to `~/.claude/rules/develop-config.md` (single-file symlinks require Developer Mode or Admin on Windows).
- **Optional custom agent wrappers (all assistants):** Separate custom agent files are not shipped or required. See Section 3 of [docs/harness.md](docs/harness.md) if you want optional local wrappers in Claude Code, VS Code / GitHub Copilot, or Cursor.

---

## Step 4: Run post-install validation

Immediately after installation (and whenever skills are updated or reconfigured), read and execute **[docs/validation.md](docs/validation.md)**.

Report the full PASS / WARN / FAIL table to the user before declaring installation complete. Remind the user to open a **new chat session** (or reload the IDE window) so the coding assistant refreshes its discovered skill catalog.

Finally, show the user where to find the two developer aides so they can start using the kit immediately:

- **System overview (how the pieces fit together):** [docs/overview.md](docs/overview.md) and visual diagram [docs/assets/architecture-overview.svg](docs/assets/architecture-overview.svg)
- **Quick reference (all 20 `/` commands, when to use them, and how to find inputs):** [docs/quick-reference.md](docs/quick-reference.md)
- **Printable 2-page handout (PDF):** [docs/handouts/agent-skills-handout.pdf](docs/handouts/agent-skills-handout.pdf) (also browsable at `https://github.com/uw-loci/agent-skills/blob/main/docs/handouts/agent-skills-handout.pdf`)
- **Tip:** You can invoke any `/` command bare (with no arguments) or read its `/` menu description to see what inputs it expects before it edits any files.

---

## Reconfiguring later

To change models, `parallel_subagents`, `delegation_policy`, or `default_contexts` later, edit `~/.agents/develop-config.md` directly (or `<target-repo>/.agents/develop-config.md` for a project-local overlay), ask an agent to update it, or run `/context configure` to pick active context guides interactively. On Windows with Claude Code, if `~/.claude/rules/develop-config.md` is a static copy rather than a symlink, copy the updated `~/.agents/develop-config.md` over it so Claude Code stays in sync. Re-run Suite 2 of [docs/validation.md](docs/validation.md), and also re-run Suite 3 Check 5 whenever you change any subagent model value. No skill files need to be edited or relinked.

---

## Uninstalling

Uninstalling removes skill registrations, links or copies installed by this kit, Claude Code's user-global rule link (if installed), and `develop-config.md`. It leaves your local git clone untouched.

Before removing anything, read `develop-config.md` (`~/.agents/develop-config.md`, `~/.claude/rules/develop-config.md`, and any `<target>/.agents/develop-config.md`) to confirm `repo_path`, `install_scope`, and `install_method`.

1. **Remove skill registrations, links, or copies:**
   - **Antigravity (`skills-json`):** Remove only the entry matching `<REPO>/skills` from `~/.gemini/config/skills.json` (user-global) or `<target>/.agents/skills.json` (project-local), keeping all other user entries intact.
     ```powershell
     # Windows (PowerShell)
     $manifest = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath("$HOME\.gemini\config\skills.json") # or "<target>\.agents\skills.json"
     $skillsPath = (("<REPO>".TrimEnd('\', '/')) + '/skills') -replace '[\\/]+', '/'
     if (Test-Path $manifest) {
         $raw = Get-Content $manifest -Raw -Encoding UTF8
         $cfg = if ($raw -and $raw.Trim()) { $raw | ConvertFrom-Json } else { $null }
         if ($cfg -and ($cfg.PSObject.Properties.Name -contains 'entries') -and $cfg.entries) {
             $cfg.entries = @($cfg.entries | Where-Object { (($_.path -replace '[\\/]+', '/').TrimEnd('/')) -ine $skillsPath })
             $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
             [System.IO.File]::WriteAllText($manifest, ($cfg | ConvertTo-Json -Depth 5), $utf8NoBom)
         }
     }
     ```
     On macOS or Linux, remove the matching `<REPO>/skills` object from the `"entries"` array in `~/.gemini/config/skills.json` (or `<target>/.agents/skills.json`).
   - **Symlinks or Windows directory junctions (`symlink` / `junction`):** Remove only links under `<DEST>` whose names match directories in `<REPO>/skills/`. Never delete non-link directories or unrelated user skills.
     ```powershell
     # Windows (PowerShell)
     $dest = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath("<DEST>")
     Get-ChildItem -Directory "<REPO>\skills" | ForEach-Object {
         $target = Join-Path $dest $_.Name
         $item = Get-Item -LiteralPath $target -Force -ErrorAction SilentlyContinue
         if ($item -and ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
             [System.IO.Directory]::Delete($target)
         }
     }
     ```
     ```bash
     # macOS / Linux (POSIX shell)
     for d in "<REPO>"/skills/*/; do
         [ -d "$d" ] || continue
         target="<DEST>/$(basename "$d")"
         if [ -L "$target" ]; then
             rm "$target"
         fi
     done
     ```
   - **Static copies (`copy`):** Delete only the 20 skill directories matching `<REPO>/skills/` inside `<DEST>` after confirming with the user that no local edits need to be kept.
2. **Remove Claude Code's config rule link and any custom agent wrappers (if installed):**
   - **Claude Code (user-global only):** Delete `~/.claude/rules/develop-config.md`.
   - **Any assistant (optional or legacy cleanup):** If you manually created optional custom agent wrappers (or upgraded from v1.0-1.2 where `develop-agent` or `comment-auditor` were linked), delete them from your assistant's `agents/` directory.
3. **Delete `develop-config.md`:** Remove `~/.agents/develop-config.md` (user-global) or `<target>/.agents/develop-config.md` (project-local).
4. **Reload the coding assistant:** Start a new chat session (or reload the IDE window) so the assistant clears the uninstalled skills from its catalog.

---

## Maintaining this repository (for contributors and agents)

Follow these rules when editing `uw-loci/agent-skills` itself (skip during normal end-user installation):

- **Single source of truth for commands:** All 20 commands live in `skills/*/SKILL.md` and are documented once in [docs/quick-reference.md](docs/quick-reference.md). Do not duplicate the full 20-command table in `README.md`.
- **Rebuilding the 2-page PDF handout:** Whenever you change `skills/*/SKILL.md` frontmatter, `docs/quick-reference.md`, `docs/assets/architecture-overview.svg`, `scripts/handout-template.html`, or `plugin.json`, regenerate `docs/handouts/agent-skills-handout.pdf` and verify freshness before committing:
  ```bash
  # Use `uv run --no-project python` if Python is managed via uv
  python scripts/build-handouts.py
  python scripts/build-handouts.py --check
  ```
- **CI enforcement:** [.github/workflows/ci.yml](.github/workflows/ci.yml) runs `python3 scripts/build-handouts.py --check` on every push and pull request (failing if skills, links, SVG XML, stale refs, or the PDF input fingerprint drift), and rebuilds the PDF on `main` or manual workflow dispatch when stale.
- **Validation:** Run [docs/validation.md](docs/validation.md) Suite 1 before shipping changes to this repository.
