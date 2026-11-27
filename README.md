# uw-loci/agent-skills

A curated, portable set of coding-assistant skills, workflows, engineering principles, and UW-LOCI project guides for **VS Code / GitHub Copilot**, **Antigravity**, **Claude Code**, **Cursor**, and other [Agent Skills](https://agentskills.io)-compatible coding assistants.

These skills give developers (from students to seasoned engineers) repeatable workflows for planning, debugging, reviewing, documenting, and verifying code, with built-in token-usage controls and an immutable live-linked install model. Derived from [`cursor/plugins/pstack`](https://github.com/cursor/plugins/tree/main/pstack) (via [`backnotprop/pstack`](https://github.com/backnotprop/pstack)), this repository trims the upstream catalog to **20 Agent Skills** centered on `/develop`, **7 playbooks**, **14 engineering principles**, and **5 development context guides**.

## Quick start (agent-assisted installation)

1. Clone this repository to a stable location on your machine:
   ```bash
   # HTTPS (works everywhere, no SSH key needed)
   git clone https://github.com/uw-loci/agent-skills.git

   # Or SSH
   git clone git@github.com:uw-loci/agent-skills.git
   ```
2. Open the cloned repository in your coding assistant (**Antigravity**, **VS Code / GitHub Copilot**, **Claude Code**, **Cursor**, or another Agent Skills-compatible assistant) and ask:
   ```text
   Read AGENTS.md and install these skills for me.
   ```
3. The assistant detects your coding assistant and OS, then walks through one decision per question:
   - Confirm your active coding assistant and whether to install globally or inside one repository
   - Keep skills live-linked to this git clone (`git pull` updates automatically) or install a static copy
   - Choose when workflows delegate bulky edits to a helper subagent (`adaptive`, `single-agent`, or `always-delegate`)
   - Choose how many parallel subagents multi-agent workflows start (default `2`)
   - Choose whether subagents reuse your active chat model (`inherit`) or use specific assistant-supported models for high, medium, and low effort tiers
   - Choose whether UW-LOCI ecosystem and language context guides load automatically (`auto`), use guides picked from a checklist, or stay manual (`none`)
4. The assistant writes your preferences to an external config file (`~/.agents/develop-config.md`, plus a linked rule for Claude Code), links all 20 skills, and runs [docs/validation.md](docs/validation.md) to verify every skill, link, and configured subagent model.
5. Start a **new chat session** (or reload your IDE window) so your coding assistant loads the newly linked skills.

> **Updating later:** Run `git pull` inside your clone, then ask an assistant to run [docs/validation.md](docs/validation.md). Edit `develop-config.md` at any time (or run `/context configure`) to adjust models, parallel subagents, delegation policy, or context guides without modifying any skill files. To uninstall cleanly, see the **Uninstalling** section in [AGENTS.md](AGENTS.md).

## How to use it (examples)

After restarting your coding assistant, invoke any skill with its `/` command. For `/develop`, giving three things produces the best results: **your goal**, **how to verify success (a pass/fail check)**, and **any constraints**. If you leave details out, `/develop` asks brief follow-up questions before editing code.

```text
/develop Fix the axis-order mismatch in fiber_angles() when given 3D (Z, Y, X) arrays.
Done check: uv run pytest tests/test_angles.py passes including a new 3D regression test.
Constraint: preserve existing 2D public signatures.
```

Other common entry points:

```text
/how How does image loading dispatch between Bio-Formats and SCIFIO here?
/sharpen Refactor the plugin registration layer so it is easier to test.
/interrogate
/audit-comments src/pycurvelets/angles.py
/context configure
```

## What is included

### Router and playbooks (`/develop`)

[`skills/develop/SKILL.md`](skills/develop/SKILL.md) is the main entry point for non-trivial engineering work. State your goal, a pass/fail check, and any constraints (or let the agent ask for missing criteria). `/develop` picks the matching playbook, reads relevant principles from [`skills/develop/references/principles/`](skills/develop/references/principles/), and routes to specialist skills as needed.

| Playbook | File | Purpose |
|---|---|---|
| Investigation | [`playbooks/investigation.md`](skills/develop/playbooks/investigation.md) | Read-only architecture or history analysis, or tradeoffs comparison |
| Bug fix | [`playbooks/bug-fix.md`](skills/develop/playbooks/bug-fix.md) | Reproduce first, isolate root cause, apply minimal fix, prove on the real runtime path |
| Feature | [`playbooks/feature.md`](skills/develop/playbooks/feature.md) | Design data shape first, implement per delegation policy, verify end to end |
| Refactoring | [`playbooks/refactoring.md`](skills/develop/playbooks/refactoring.md) | Pin behavior contract first, subtract dead code, reshape cleanly, prove equivalence |
| Prototype | [`playbooks/prototype.md`](skills/develop/playbooks/prototype.md) | Fast throwaway experiment to settle design or behavioral forks cheaply |
| Multi-phase plan | [`playbooks/multi-phase-plan.md`](skills/develop/playbooks/multi-phase-plan.md) | Ordered, verifiable phase or PR plan (plan only, no code changes) |
| Opening a PR | [`playbooks/opening-a-pr.md`](skills/develop/playbooks/opening-a-pr.md) | Clean diff, small logical commits, conventional title, concise briefing body |

### All 20 skills

| Category | Skill | Purpose and typical input |
|---|---|---|
| **Router** | [`/develop`](skills/develop/SKILL.md) | Main workflow router (7 playbooks and 14 principles); pass goal, pass/fail check, and constraints |
| **Context** | [`/context`](skills/context/SKILL.md) | Load or configure UW-LOCI repo guides and Java/Python conventions (`/context`, `/context <slug>`, or `/context configure`) |
| | [`/create-context-guide`](skills/create-context-guide/SKILL.md) | Create or update an ecosystem repo map or language guide and register it in `/context` |
| **Understand** | [`/how`](skills/how/SKILL.md) | Cited architecture walkthrough of how a subsystem works or where code belongs |
| | [`/why`](skills/why/SKILL.md) | Cited design rationale and history from git commits and PR discussions |
| | [`/teach`](skills/teach/SKILL.md) | Plain-language, step-by-step explanation with incremental diagrams built on `/how` and `/why` |
| **Frame and design** | [`/in-your-own-words`](skills/in-your-own-words/SKILL.md) | Restate your goal and problem in plain language and pause for confirmation before editing |
| | [`/sharpen`](skills/sharpen/SKILL.md) | Rewrite an underspecified prompt into a deeper, verifiable prompt without executing it |
| | [`/architect`](skills/architect/SKILL.md) | Compare two structural designs (types, signatures, module boundaries) and pause for approval |
| | [`/blast-radius`](skills/blast-radius/SKILL.md) | Find hidden downstream breakage beyond a diff and prove the core safety assumption with code (defaults to current branch diff) |
| | [`/arena`](skills/arena/SKILL.md) | Run parallel independent attempts on a hard task, grade against a rubric, and combine the best parts |
| **Build and verify** | [`/tdd`](skills/tdd/SKILL.md) | Write a failing test first, confirm it fails, then implement the fix (skips brittle tests when no cheap path exists) |
| | [`/interrogate`](skills/interrogate/SKILL.md) | Adversarial diff or design review where only run-proven findings survive (defaults to current branch diff) |
| | [`/create-verification-skill`](skills/create-verification-skill/SKILL.md) | Generate a project-local `verify-<app>` skill to launch and test your app, CLI, desktop tool, or library end to end |
| | [`/maintain-verification-skill`](skills/maintain-verification-skill/SKILL.md) | Audit and update a project's `verify-<app>` skill and feature map against source and live runs |
| **Clean and write** | [`/audit-comments`](skills/audit-comments/SKILL.md) | Audit comments and suppressions, then ask before deleting clutter or fixing underlying workarounds (defaults to current branch diff) |
| | [`/unslop`](skills/unslop/SKILL.md) | Rewrite prose to remove common AI writing patterns, filler, and vague wording |
| | [`/technical-writing`](skills/technical-writing/SKILL.md) | Write or edit docs, READMEs, RFCs, PRs, and commits using the four-mode Diátaxis doc framework and clear, unambiguous sentences |
| **Team learning** | [`/correct`](skills/correct/SKILL.md) | Turn repeated agent mistakes into permanent checks (architecture, types, lint, or tests); proposes fixes for approval first |
| | [`/reflect`](skills/reflect/SKILL.md) | Review a working session for lasting lessons and propose targeted skill edits for approval |

### Development context guides (5)

Indexed in [`skills/context/SKILL.md`](skills/context/SKILL.md) and loaded on demand so `/` menus stay uncluttered and unrelated repo maps stay out of the context window:

- **Ecosystems:**
  - [`fiji-imagej`](skills/context/references/ecosystems/fiji-imagej.md): SciJava, ImgLib2, SCIFIO, ImageJ 1.x and ImageJ2, Fiji update sites (`Fiji` stable Java 8 versus `Fiji-latest` Java 21+), Ops lineage (`imagej-ops`, `scijava-ops`, `scikit-ops`), PyImageJ and ScyJava, and Appose, Jaunch, and jgo.
  - [`tme-quant`](skills/context/references/ecosystems/tme-quant.md): `uw-loci/tme-quant` (active Python core), `fiji-curvealign` (priority Fiji connector), `napari-curvealign` (on hold), `curvelets` (MATLAB reference), and CurveLab/MATLAB parity testing rules.
  - [`qupath`](skills/context/references/ecosystems/qupath.md) *(starter draft, awaiting QuPath lead review)*: UW-LOCI QuPath extensions, the Gradle convention plugin exception, Appose Python workers, and strict read-only and no-AI-upstream boundaries for `qupath/qupath`.
- **Languages:**
  - [`java`](skills/context/references/languages/java.md): Maven and `pom-scijava` Bill of Materials (BOM) discipline, Java 8 versus 21 checks, SciJava Inversion of Control (IoC) lifecycle, ImgLib2 hot-loop hygiene, and `scijava-coding-style` pointers.
  - [`python`](skills/context/references/languages/python.md): `uv`, `ruff`, `pytest`, scientific array and axis discipline, MATLAB-porting pitfalls, headless Qt and `napari` testing rules, and Java interop boundaries.

### Curated engineering principles (14)

Stored under [`skills/develop/references/principles/`](skills/develop/references/principles/) (rather than top-level slash skills) so `/` command menus stay uncluttered across coding assistants:

- **Core:** Laziness Protocol (code as a liability and single source of truth), Foundational Thinking, Redesign from First Principles, Minimize Reader Load (including least surprise in function contracts)
- **Open Science:** Reproducible, Immutable Artifacts (Findable, Accessible, Interoperable, Reusable [FAIR] hygiene, separation of concerns, Semantic Versioning, and snapshot/dev versioning), Accessible by Design (principle of least surprise, scientist-first UX, actionable errors, and confirming risky side effects)
- **Architecture:** Model the Domain, Boundary Discipline (including failing loudly instead of silent coercion or fallback), Separate Before Serializing Shared State
- **Verification:** Prove It Works, Fix Root Causes, Sequence Verifiable Units, Test Behavior Not Implementation
- **Delegation:** Guard the Context Window

## Documentation

- **[AGENTS.md](AGENTS.md):** Agent-facing installation, interactive configuration, and uninstallation guide.
- **[docs/harness.md](docs/harness.md):** Skill discovery paths, Windows setup notes, and guidance on optional user-created custom agent wrappers across VS Code / GitHub Copilot, Antigravity, Claude Code, Cursor, and other Agent Skills assistants.
- **[skills/develop/references/config-and-subagents.md](skills/develop/references/config-and-subagents.md):** Single runtime reference for config lookup and merging, effort tiers, supported model values, tool mappings, transcript locations, and fallbacks.
- **[docs/validation.md](docs/validation.md):** Three-suite read-only validation checklist for verifying repository integrity, installation links, config, and live subagent wiring.
- **[CHANGELOG.md](CHANGELOG.md):** Full record of this repository's changes and upstream components intentionally omitted.

## TODO / Roadmap

- [ ] **Human-facing quick-reference handout:** Create a concise 1-page team quick-reference (prompt checklist covering goal, pass/fail check, constraints, context, and verification; command cheat sheet; token guardrails; and copy-paste recipes) once the skill set has been field-tested across the team.

## License

MIT (see [LICENSE](LICENSE)). Derived from `cursor/plugins/pstack` by Lauren Tan (Poteto) and `backnotprop/pstack`.
