---
name: create-context-guide
description: "Create or update a concise development context guide (ecosystem repo map or language conventions) under skills/context/references/ and register it in skills/context/SKILL.md. Use for /create-context-guide or when onboarding a new multi-repo stack or team domain."
disable-model-invocation: true
---

# Create a context guide

Multi-repo ecosystems are opaque to an agent opened inside a single repository. A good context guide gives future agents a compact, evergreen map of repository boundaries, tooling invariants, and community policies without bloating their context window.

Target destination inside this kit:
- **Ecosystem guide:** `../context/references/ecosystems/<slug>.md`
- **Language guide:** `../context/references/languages/<slug>.md`
- **Index registration:** `../context/SKILL.md`

If installed via symlink/junction, check `repo_path` in `develop-config.md` so edits land in the version-controlled fork repository (never commit or push without explicit user approval).

## 1. Interview the domain owner and inspect existing repos

Gather facts from local checkouts, repo READMEs/POMs/`pyproject.toml` files, or org listings first; ask the user only for what code cannot tell you:

1. **Scope & triggers:** Which GitHub orgs, repositories, package names, or domain terms should activate this guide?
2. **Layering & ownership:** What builds on what? Which repos are active priorities, which are thin connectors, and which are legacy/archived/on-hold?
3. **Where to look for X:** What are the 5-15 most common "where does this live?" routing answers (shared CI/release scripts, coding style repos, BOM/version catalogs, docs/wikis, launchers, core libraries)?
4. **Build, test & runtime invariants:** Build tool (Maven vs. Gradle, `uv` vs. `conda`), target language/JDK versions, split release channels, special test flags, headless GUI constraints, or cross-repo local dev steps.
5. **Upstream policy & contribution boundaries (mandatory question):** Are there upstream licensing constraints, external binary restrictions, or community/anti-AI policies (such as read-only upstream repos where AI-generated PRs/issues are prohibited)?

## 2. Draft the guide (keep it dense and under ~150 lines)

Write for a cold agent entering one repo in the ecosystem for the first time. Cut generic textbook advice and volatile details (transient issue numbers, specific line numbers, short-lived branch names).

Use this structure for **ecosystem guides**:

1. **Title & companion guides:** Name sibling language or ecosystem guides to load alongside this one.
2. **Scope & triggers:** Concrete org/repo/keyword triggers.
3. **Architecture & layering:** One compact ASCII diagram showing dependency direction and active vs. legacy boundaries.
4. **Where to look for X:** A concise Markdown table (`Repository | Role & status | When to touch it`) with verified links.
5. **Critical invariants & sharp edges:** Only non-obvious rules that would trip an agent on turn 1 (version splits, BOM/tooling rules, test flags, interop boundaries).
6. **Upstream policy & contribution boundaries:** Explicit rules on external repos, licensing, and AI contribution policies.

If any detail could not be verified from code or the domain owner yet, mark it visibly under an **Open items for maintainer review** checklist rather than guessing.

Apply the **unslop** skill to strip filler and vague prose.

## 3. Register and verify

1. Add or update the guide's row in [`../context/SKILL.md`](../context/SKILL.md) with accurate triggers and relative path.
2. Verify every relative path and every checked repository URL is accurate.
3. Update `docs/validation.md` expected inventory if the guide is part of the committed team baseline.
4. Present the drafted guide, the registration diff, and any unverified open items for the domain owner to review before committing.
