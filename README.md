# uw-loci/agent-skills

A curated, cross-harness engineering skill kit adapted from [`cursor/plugins/pstack`](https://github.com/cursor/plugins/tree/main/pstack) (via [`backnotprop/pstack`](https://github.com/backnotprop/pstack)) for teams working across **VS Code / GitHub Copilot**, **Antigravity**, **Claude Code**, **Cursor**, and other [Agent Skills](https://agentskills.io)-compatible harnesses.

This fork trims upstream `pstack` down to a practical core of **20 Agent Skills** centered on `/develop`, **7 playbooks**, **14 engineering principles**, **5 development context guides**, and **2 subagent definitions**, with explicit token-usage controls and an immutable symlink-based installation model.

## Quick start (agent-assisted installation)

1. Clone this repository to a stable location on your machine:
   ```bash
   git clone git@github.com:uw-loci/agent-skills.git
   ```
2. Open the cloned repository in your coding agent (**Antigravity**, **VS Code / GitHub Copilot**, **Claude Code**, **Cursor**, or another Agent Skills-compatible harness) and ask:
   ```text
   Read AGENTS.md and install these skills for me.
   ```
3. The agent will confirm your detected environment and ask you for:
   - Confirmation of the active harness and install scope (user-global vs. project-local)
   - Link method (symlink / Windows directory junction by default so `git pull` keeps everything current without mutating skills)
   - Delegation policy (`adaptive`, `single-agent`, or `always-delegate`)
   - Per-role model preferences (`inherit-parent` by default)
   - Orchestrator panel counts for `/interrogate` and `/arena`
   - Default development context guides (`auto` by default, or explicit slugs)
4. The agent writes your choices to an external config file (`~/.agents/develop-config.md`, plus a linked rule for Claude Code), links all 20 skills, and runs [docs/validation.md](docs/validation.md) to verify every skill and link.
5. Start a **new chat session** (or reload your IDE window) so your harness picks up the newly linked skills.

> **Updating later:** Run `git pull` inside your clone, then ask an agent to run [docs/validation.md](docs/validation.md). Edit `develop-config.md` at any time to adjust models, panel counts, or delegation policy without touching any skill files.

## What is included

### Router & playbooks (`/develop`)

[`skills/develop/SKILL.md`](skills/develop/SKILL.md) is the main entry point for non-trivial engineering work. State your goal, a pass/fail done check, and any constraints; `/develop` selects a playbook, loads relevant principles from [`skills/develop/references/principles/`](skills/develop/references/principles/), and invokes specialist skills as needed.

| Playbook | File | Purpose |
|---|---|---|
| Investigation | [`playbooks/investigation.md`](skills/develop/playbooks/investigation.md) | Read-only architecture or history analysis, or tradeoffs comparison |
| Bug fix | [`playbooks/bug-fix.md`](skills/develop/playbooks/bug-fix.md) | Reproduce first, isolate root cause, apply minimal fix, prove on the real surface |
| Feature | [`playbooks/feature.md`](skills/develop/playbooks/feature.md) | Design data shape first, implement per delegation policy, verify end to end |
| Refactoring | [`playbooks/refactoring.md`](skills/develop/playbooks/refactoring.md) | Pin behavior contract first, subtract dead code, reshape cleanly, prove equivalence |
| Prototype | [`playbooks/prototype.md`](skills/develop/playbooks/prototype.md) | Fast throwaway experiment to settle design or behavioral forks cheaply |
| Multi-phase plan | [`playbooks/multi-phase-plan.md`](skills/develop/playbooks/multi-phase-plan.md) | Ordered, verifiable phase/PR plan (plan only, no code changes) |
| Opening a PR | [`playbooks/opening-a-pr.md`](skills/develop/playbooks/opening-a-pr.md) | Clean diff, small logical commits, conventional title, concise briefing body |

### All 20 skills

| Category | Skill | Purpose |
|---|---|---|
| **Router** | [`/develop`](skills/develop/SKILL.md) | Primary workflow router (7 playbooks + 14 engineering principles) |
| **Context** | [`/context`](skills/context/SKILL.md) | Progressively loads UW-LOCI multi-repo ecosystem maps and Java/Python conventions |
| | [`/create-context-guide`](skills/create-context-guide/SKILL.md) | Interview a domain owner, inspect repos, and author or update a context guide |
| **Understand** | [`/how`](skills/how/SKILL.md) | Architectural walkthrough of how a subsystem works |
| | [`/why`](skills/why/SKILL.md) | Cited rationale and history from git commits and PR records |
| | [`/teach`](skills/teach/SKILL.md) | Plain, diagram-by-diagram explanation built on `/how` and `/why` |
| **Frame & Design** | [`/in-your-own-words`](skills/in-your-own-words/SKILL.md) | Play back goals and problem statement before editing code |
| | [`/sharpen`](skills/sharpen/SKILL.md) | Deepen an underspecified prompt before sending it |
| | [`/architect`](skills/architect/SKILL.md) | Settle types, signatures, and module boundaries before writing code |
| | [`/blast-radius`](skills/blast-radius/SKILL.md) | Find hidden downstream breakage and prove the core safety fact with code |
| | [`/arena`](skills/arena/SKILL.md) | Run parallel candidate designs/implementations and synthesize the best shape |
| **Build & Verify** | [`/tdd`](skills/tdd/SKILL.md) | Write a failing regression test first when a cheap local test path exists |
| | [`/interrogate`](skills/interrogate/SKILL.md) | Adversarial diff/design review where only run-proven bugs survive |
| | [`/create-verification-skill`](skills/create-verification-skill/SKILL.md) | Generate a project-local `verify-<app>` skill to drive and prove real app behavior |
| | [`/maintain-verification-skill`](skills/maintain-verification-skill/SKILL.md) | Keep a project-local verification skill and feature map in sync with the app |
| **Clean & Write** | [`/no-comments`](skills/no-comments/SKILL.md) | Audit comments and suppressions via Comment Auditor; fix accepted root causes |
| | [`/unslop`](skills/unslop/SKILL.md) | Strip AI writing tells and filler from prose |
| | [`/technical-writing`](skills/technical-writing/SKILL.md) | Layered doc standard (Diátaxis, Google style, STE, Global English) |
| **Team Learning** | [`/correct`](skills/correct/SKILL.md) | Turn repeated agent mistakes into structural checks (types, lint, tests) |
| | [`/reflect`](skills/reflect/SKILL.md) | Distill durable session lessons into concrete skill improvements |

### Development context guides (5)

Stored under [`skills/context/references/`](skills/context/SKILL.md) and loaded on demand so `/` menus stay clean and unrelated repo maps stay out of the context window:

- **Ecosystems:**
  - [`fiji-imagej`](skills/context/references/ecosystems/fiji-imagej.md) — SciJava, ImgLib2, SCIFIO, ImageJ 1.x/2, Fiji update sites (`Fiji` stable Java 8 vs. `Fiji-latest` Java 21+), Ops lineage (`imagej-ops` / `scijava-ops` / `scikit-ops`), PyImageJ/ScyJava, and Appose/Jaunch/jgo.
  - [`tme-quant`](skills/context/references/ecosystems/tme-quant.md) — `uw-loci/tme-quant` (active Python core), `fiji-curvealign` (priority Fiji connector), `napari-curvealign` (on hold), `curvelets` (MATLAB reference), and CurveLab/MATLAB parity testing rules.
  - [`qupath`](skills/context/references/ecosystems/qupath.md) — Starter draft (awaiting QuPath lead review) covering UW-LOCI QuPath extensions, the Gradle convention plugin exception, Appose Python workers, and strict read-only / no-AI-upstream boundaries for `qupath/qupath`.
- **Languages:**
  - [`java`](skills/context/references/languages/java.md) — Maven & `pom-scijava` BOM discipline, Java 8 vs. 21 checks, SciJava IoC lifecycle, ImgLib2 hot-loop hygiene, and `scijava-coding-style` pointers.
  - [`python`](skills/context/references/languages/python.md) — `uv`, `ruff`, `pytest`, scientific array/axis discipline, MATLAB-porting pitfalls, headless Qt/`napari` testing rules, and Java interop boundaries.

### Curated engineering principles (14)

Stored under [`skills/develop/references/principles/`](skills/develop/references/principles/) (rather than top-level slash skills) so `/` command menus stay uncluttered across harnesses:

- **Core:** Laziness Protocol (code as a liability & single source of truth), Foundational Thinking, Redesign from First Principles, Minimize Reader Load
- **Open Science:** Reproducible, Immutable Artifacts (FAIR, separation of concerns, SemVer & snapshot/dev versioning), Accessible by Design (scientist-first UX & actionable errors)
- **Architecture:** Model the Domain, Boundary Discipline, Separate Before Serializing Shared State
- **Verification:** Prove It Works, Fix Root Causes, Sequence Verifiable Units, Test Behavior Not Implementation
- **Delegation:** Guard the Context Window

### Subagent definitions (2)

- [`agents/develop-agent.md`](agents/develop-agent.md) — Scoped delegate spawned by `/develop` when delegating implementation.
- [`agents/comment-auditor.md`](agents/comment-auditor.md) — Read-only comment and suppression auditor used by `/no-comments` (also mirrored inside `skills/no-comments/references/comment-auditor.md` for harnesses without static agent files).

## Documentation

- **[AGENTS.md](AGENTS.md)** — Agent-facing installation and interactive configuration procedure.
- **[docs/harness.md](docs/harness.md)** — Discovery paths, tool mappings, and model syntax for VS Code / GitHub Copilot, Antigravity, Claude Code, Cursor, and other Agent Skills-compatible harnesses.
- **[docs/validation.md](docs/validation.md)** — Post-install and integration validation checklist for verifying skills, links, config, and subagent wiring.
- **[CHANGELOG.md](CHANGELOG.md)** — Full record of this fork's refactoring and every upstream component intentionally omitted.

## TODO / Roadmap

- [ ] **Human-facing quick-reference handout:** Create a concise 1-page team quick-reference (5-part prompt formula, command cheat sheet, token guardrails, and copy-paste recipes) once the core skill set has been field-tested across the team.

## License

MIT (see [LICENSE](LICENSE)). Derived from `cursor/plugins/pstack` by Lauren Tan (Poteto) and `backnotprop/pstack`.
