---
name: create-context-guide
description: "Create or update a concise ecosystem repository map or language convention guide and register it in /context. Pass the ecosystem or language name after /create-context-guide."
disable-model-invocation: true
---

# Create a context guide

Multi-repo ecosystems are opaque to an agent opened inside a single repository. A good context guide gives future agents a compact, evergreen map of repository boundaries, tooling invariants, and community policies without bloating the context window.

If the user invokes `/create-context-guide` without naming a target stack or language, ask whether they want an **ecosystem guide** or a **language guide** and which repositories or language it covers before starting.

Target destinations inside this kit:

- **Ecosystem guide:** `../context/references/ecosystems/<slug>.md`
- **Language guide:** `../context/references/languages/<slug>.md`
- **Index registration:** `../context/SKILL.md`

**Installation destination note:** Resolve `repo_path` and `install_method` from `develop-config.md` per [`../develop/references/config-and-subagents.md`](../develop/references/config-and-subagents.md).
- **Live-linked clone (`skills.json`, symlink, or directory junction):** Write edits inside `<repo_path>/skills/context/` on a feature branch rather than leaving uncommitted edits on `main` (uncommitted edits under `skills/` block clean `git pull` updates and fail `<repo_path>/docs/validation.md` Suite 2 Check 4). Never commit or push without explicit user approval.
- **Static copy:** Never edit inside a read-only plugin cache. Write to your installed skill folder (`.agents/skills/context/`, `.claude/skills/context/`, `.cursor/skills/context/`, `.github/skills/context/`, or user-global equivalent) and note whether the new guide should be upstreamed to `uw-loci/agent-skills`.

## 1. Interview the domain owner and inspect existing repos

Gather facts from local checkouts, repo READMEs, `pom.xml`, `build.gradle.kts`, `pyproject.toml`, or org listings first. Ask the user only for what code cannot tell you:

1. **Scope and triggers:** Which GitHub orgs, repositories, package names, or domain terms should activate this guide?
2. **Layering and ownership:** What builds on what? Which repos are active priorities, which are thin connectors, and which are legacy, archived, or on hold?
3. **Where to look for X:** What are the 5 to 15 most common "where does this live?" routing answers (shared CI or release scripts, coding style repos, BOM or version catalogs, docs, launchers, core libraries)?
4. **Build, test, and runtime invariants:** Build tool (Maven versus Gradle, `uv` versus `conda`), target language or JDK versions, split release channels, special test flags, headless GUI constraints, or cross-repo local dev steps.
5. **Upstream policy and contribution boundaries (mandatory question):** Are there upstream licensing constraints, external binary restrictions, or community anti-AI policies (such as read-only upstream repos where AI-generated PRs or issues are prohibited)?

## 2. Draft the guide (keep it dense and under ~150 lines)

Write for a cold agent entering one repo in the ecosystem for the first time. Cut generic textbook advice and volatile details (transient issue numbers, specific line numbers, short-lived branch names).

Use this structure for **ecosystem guides**:

1. **Title and companion guides:** Name sibling language or ecosystem guides to load alongside this one.
2. **Scope and triggers:** Concrete org, repo, and keyword triggers.
3. **Architecture and layering:** One compact ASCII diagram showing dependency direction and active versus legacy boundaries.
4. **Where to look for X:** A concise Markdown table (`Repository | Role and status | When to touch it` or `Need / Subsystem | Repository / Source | Notes`) with verified links.
5. **Critical invariants and sharp edges:** Only non-obvious rules that would trip an agent on turn 1 (version splits, BOM or tooling rules, test flags, interop boundaries).
6. **Upstream policy and contribution boundaries:** Explicit rules on external repos, licensing, and AI contribution policies.

Use this structure for **language guides**:

1. **Title and scope:** Target language, repos covered, and linters/formatters to defer standard style to.
2. **Tooling and dependency management:** Build tool, package manager, version checks, and BOM or lockfile rules.
3. **Ecosystem idioms and sharp edges:** Non-obvious naming, compatibility, versioning, performance, or domain pitfalls.
4. **Testing and verification:** Standard test commands, headless constraints, and multi-repo local verification.

If any detail cannot be verified from code or the domain owner yet, mark it visibly under an **Open items for maintainer review** checklist and flag the guide as a starter draft rather than guessing.

Apply the **unslop** skill to strip filler and vague prose.

## 3. Register and verify

1. Add or update the guide's row in [`../context/SKILL.md`](../context/SKILL.md) (including `(starter draft)` if unverified items remain), and update `../context/SKILL.md`'s frontmatter `description:` if a new major ecosystem or language was added.
2. Verify every relative path and every checked repository URL is accurate.
3. If the guide is part of the committed team baseline inside `<repo_path>`, update the context-guide list, hardcoded count checks in the Suite 1 PowerShell and Bash scripts in `<repo_path>/docs/validation.md`, and counts in `<repo_path>/README.md` and `<repo_path>/AGENTS.md`.
4. Present the drafted guide, the registration diff, and any unverified open items for the domain owner to review before committing.
