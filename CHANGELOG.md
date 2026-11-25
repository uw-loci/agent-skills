# Changelog

All notable changes in `uw-loci/agent-skills` (the UW-LOCI team fork of `pstack`) are documented here.

## [1.2.0] — Open-Source Science Principles & Ecosystem Refinements

Tuned the engineering principles, refactoring playbook, and ecosystem guides for open-source scientific software, aligned with [`imagej.net/develop/`](https://imagej.net/develop/) and [`uw-loci.github.io`](https://uw-loci.github.io/).

### Added

- Two open-science engineering principles under `skills/develop/references/principles/` (bringing the curated set from 12 to **14**):
  - `reproducible-immutable-artifacts.md` — Immutable releases and shared git history, FAIR hygiene, algorithm/GUI separation of concerns, SemVer backward compatibility for mature (`>= 1.0`) public APIs, and immediate `-SNAPSHOT` / `.dev0` version advancement when API scope grows.
  - `accessible-by-design.md` — Scientist-first UX across GUI, CLI, and library entry points, sensible defaults and explicit units, actionable errors, low-friction distribution, and extensibility over one-offs.

### Updated

- `skills/develop/references/principles/laziness-protocol.md` — Encoded LOCI's "code is a maintenance liability" rule: ask *"where does this belong?"* first, reuse/depend on existing stack components when appropriate without blindly searching upstream on every edit, and maintain a single source of truth instead of diverging forks.
- `skills/develop/references/principles/redesign-from-first-principles.md` & `skills/develop/playbooks/refactoring.md` — Scoped one-wave API deletion strictly to internal and `0.x` incubating APIs while requiring SemVer deprecation and compatibility for mature (`>= 1.0`) public APIs.
- `skills/develop/references/principles/boundary-discipline.md` — Explicitly named GUI frameworks (Swing, JavaFX, napari) and IPC bridges (Appose, PyImageJ/ScyJava) as thin outer adapters around UI-agnostic core algorithms.
- `skills/develop/references/principles/fix-root-causes.md` — Added minimal data reduction and state isolation guidance for debugging large scientific datasets.
- `skills/context/references/ecosystems/fiji-imagej.md` & `skills/context/references/languages/java.md` — Documented the temporary `pom-scijava` version-property override convention (pin when a newer component release predates `pom-scijava`, then audit and remove pins on BOM bumps), SemVer `-SNAPSHOT` checks, and shared portals (`search.imagej.net`, `javadoc.scijava.org`, `imagej.net/develop/`, `uw-loci.github.io`, `forum.image.sc`, `imagesc.zulipchat.com`).
- Synced counts and references across `skills/develop/SKILL.md`, `AGENTS.md`, `README.md`, `docs/validation.md`, and `plugin.json` (`1.2.0`).

---

## [1.1.1] — Repository Rename

- Renamed repository references, clone instructions, and plugin metadata from `uw-loci/pstack` to `uw-loci/agent-skills` across `README.md`, `AGENTS.md`, `plugin.json`, `docs/validation.md`, and `CHANGELOG.md`.

---

## [1.1.0] — UW-LOCI Development Context Guides & Language Conventions

Added progressive-disclosure multi-repo context maps and UW-LOCI Java/Python conventions under a unified `context` skill plus a `/create-context-guide` authoring workflow, bringing the kit to **20 skills**.

### Added

- **`skills/context/`** — Lightweight progressive-disclosure router (`SKILL.md`, model-invocable and callable via `/context <slug>`) housing 5 concise reference guides so `/` menus stay uncluttered and unrelated repo maps stay out of context:
  - `references/ecosystems/fiji-imagej.md` — Maps the multi-org Fiji/ImageJ/SciJava/ImgLib2/SCIFIO/Appose stack, including the `ImageJ` + `Java-8` + `Fiji` stable (Java 8 EOL) vs. `Fiji-latest` (Java 21+) update-site split, `pom-scijava` BOM sync (and obsolete `pom-fiji` warning), the three-generation Ops landscape (`imagej-ops` archived, `scijava/scijava` SciJava Ops, `apposed/scikit-ops` + `fiji-skopkit`/`napari-skopkit`), `scijava-scripts`, `scijava-coding-style`, launchers (`app-launcher`, `apposed/jaunch`, `apposed/jgo`), and Python/IPC bridges (`pyimagej`, `scyjava`, `appose`).
  - `references/ecosystems/tme-quant.md` — Maps `uw-loci/tme-quant` (active Python core), `uw-loci/fiji-curvealign` (priority Fiji connector), `uw-loci/napari-curvealign` (paused napari connector), and `uw-loci/curvelets` (MATLAB reference), including CurveLab/FFTW optional extras (`curvelops`), `TMEQ_RUN_CURVELETS`/`TMEQ_VALIDATE_MATLAB` flags, and headless Qt/`napari` test rules.
  - `references/ecosystems/qupath.md` — Starter draft (flagged for review by UW-LOCI's QuPath lead) covering `uw-loci/qupath-*` extensions, the Gradle (`qupath-gradle-plugin`) build exception, Appose Python workers, and strict read-only / no-AI-upstream contribution guardrails respecting `qupath/qupath`'s `AI_POLICY.md`.
  - `references/languages/java.md` — UW-LOCI / SciJava Java guardrails (Maven + `pom-scijava`, Java 8 vs. 21 checking, `scijava-coding-style`, SciJava IoC lifecycle, ImgLib2 allocation discipline).
  - `references/languages/python.md` — UW-LOCI Python guardrails (`uv`, `ruff`, `pytest`, scientific array axis/dtype discipline, MATLAB-porting checks, headless Qt testing, JVM/native dependency caveats).
- **`skills/create-context-guide/`** — Structured skill for interviewing domain owners, inspecting repos, capturing upstream AI/community policies, drafting `<150`-line guides, and registering them in `skills/context/SKILL.md`.

### Updated

- Wired `default_contexts` (`auto`, `none`, or comma-separated slugs) into `skills/develop/SKILL.md`, `AGENTS.md` onboarding prompts and config schema, `docs/harness.md`, `docs/validation.md` (updated for 20 skills and 5 context guides), `README.md`, and `plugin.json`.

---

## [1.0.0] — Team Core Refactoring

Refactored from upstream [`cursor/plugins/pstack`](https://github.com/cursor/plugins/tree/main/pstack) v0.15.48 (via [`backnotprop/pstack`](https://github.com/backnotprop/pstack) baseline `2a56216` / `c81f1bf`) into a focused, harness-portable skill kit for teams using **VS Code / GitHub Copilot**, **Antigravity**, and **Claude Code**.

### Major architectural changes

- **Renamed router skill to `/develop`:** Replaced `skills/poteto-mode/` with `skills/develop/` and updated all internal routing, playbooks, and cross-references.
- **Renamed subagents for team clarity:**
  - `agents/poteto-agent.md` → `agents/develop-agent.md` (removed hardcoded Cursor `model: claude-opus-5-5-xhigh-fast` header).
  - `agents/comment-sicko.md` → `agents/comment-auditor.md` (rewritten in a direct, professional tone while preserving the exact keep-list exceptions, `MUST KILL`, and `REVIEW` auditing rules; mirrored at `skills/no-comments/references/comment-auditor.md`).
- **Moved principles out of top-level slash menus:** Curated 12 core engineering principles into `skills/develop/references/principles/*.md` instead of 24 standalone `skills/principle-*` directories, keeping `/` command menus uncluttered while preserving progressive disclosure.
- **Introduced immutable-skill external configuration (`develop-config.md`):**
  - Skills remain completely unmodified in git so symlinks (or Windows directory junctions) stay clean across `git pull` updates.
  - Added a single external config file (`~/.agents/develop-config.md`, with Claude Code auto-load link at `~/.claude/rules/develop-config.md` and optional per-repo `.agents/develop-config.md` override).
  - Replaced Cursor-specific multi-vendor model slugs (`claude-opus-5-5-xhigh-fast`, `claude-fable-5-2-high`, `gemini-4-neon-xhigh`) with `inherit-parent` defaults and harness-portable tier guidance.
  - Added explicit token-usage levers: `delegation_policy` (`adaptive` default, `single-agent`, or `always-delegate`), `interrogate_reviewers` (default `2`), `arena_candidates` (default `2`), and `arena_cross_judge` (default `false`).
  - Relaxed `playbooks/feature.md`'s upstream mandatory delegation requirement so delegation follows `delegation_policy`.
- **Added agent-guided installation, harness reference, and validation docs:**
  - `AGENTS.md` — Interactive setup instructions prompting the user for harness, scope, link method, delegation policy, model choices, and orchestrator panel counts.
  - `docs/harness.md` — Unified discovery paths, tool mappings, model syntax, transcript paths, and fallbacks for VS Code / GitHub Copilot, Antigravity, and Claude Code.
  - `docs/validation.md` — Three-suite read-only validation and smoke integration checklist (repository integrity, link/config integrity, and live harness discovery + routing + optional subagent checks).
- **Cleaned cross-skill Cursor dependencies:** Removed references to `cursor-team-kit` (`/deslop`, `control-ui`, `control-cli`), Cursor `/loop`, Cursor cloud agents, Cursor Bugbot, and `.cursor/` paths across all kept skills and playbooks.

---

### Kept core inventory

- **18 skills:** `develop`, `architect`, `arena`, `blast-radius`, `correct`, `create-verification-skill`, `how`, `in-your-own-words`, `interrogate`, `maintain-verification-skill`, `no-comments`, `reflect`, `sharpen`, `tdd`, `teach`, `technical-writing`, `unslop`, `why`.
- **7 playbooks (under `skills/develop/playbooks/`):** `investigation.md`, `bug-fix.md`, `feature.md`, `refactoring.md`, `prototype.md`, `multi-phase-plan.md`, `opening-a-pr.md`.
- **12 curated principles (under `skills/develop/references/principles/`):** `laziness-protocol.md`, `foundational-thinking.md`, `redesign-from-first-principles.md`, `minimize-reader-load.md`, `model-the-domain.md`, `boundary-discipline.md`, `separate-before-serializing-shared-state.md`, `prove-it-works.md`, `fix-root-causes.md`, `sequence-verifiable-units.md`, `test-behavior-not-implementation.md`, `guard-the-context-window.md`.
- **2 agent definitions:** `agents/develop-agent.md`, `agents/comment-auditor.md`.

---

### What was intentionally left out (and why)

#### Omitted workflow & utility skills (17)

| Skill | Reason omitted |
|---|---|
| `setup-pstack` | Replaced by interactive installation in `AGENTS.md` + external `develop-config.md`. |
| `poteto-help` | Tightly coupled to upstream's 59-skill / 22-playbook catalog and Cursor Custom Modes; replaced by lean `README.md` (and planned 1-page quick-ref handout). |
| `swarm` | High-fan-out cloud-agent orchestration; deferred to keep token spend predictable and avoid unnecessary complexity during initial team adoption. |
| `figure-it-out` | Designed for multi-hour unattended runs paired with `show-me-your-work`; covered at human scale by `multi-phase-plan` and `/develop`. |
| `show-me-your-work` | TSV decision-logging script intended primarily for overnight autonomous runs. |
| `automate-me` | Mines Cursor-style session transcripts to generate personal `*-mode` skills; brittle across mixed harnesses and outside team standardization goals. |
| `recall` | Depends heavily on harness-specific cross-session transcript indexing. |
| `ketchup`, `ketchup-video` | Built for catching up on unattended/overnight runs (and video rendering pipelines). |
| `make-bot-ui` | Specific to Grok Bot webhook routines and Tailscale setups. |
| `create-formal-verification-skill`, `maintain-formal-verification-skill`, `statechart` | Specialized TLA+ / formal model-checking workflows and TypeScript chart-rendering toolchain (`skills/statechart/scripts/`); can be added back selectively if a project adopts TLA+. |
| `benchmark-checklist` | Niche performance-benchmarking audit; deferred alongside `perf-issue` and `hillclimb`. |
| `bro`, `reframe` | Optional prose/ideation utilities trimmed to keep the core command set concise (`in-your-own-words` and `sharpen` cover prompt framing). |
| `typescript-best-practices` | Language-specific skill omitted so the core kit stays language-agnostic; teams can add language-specific skills per repository as needed. |

#### Omitted playbooks (15)

| Playbooks | Reason omitted |
|---|---|
| `autonomous-run`, `autopilot-full`, `autopilot-stack`, `babysit`, `shipping` | Built around Cursor cloud VMs, `/loop`, Bugbot, and unattended PR-merging infrastructure (`watch-pr` scripts) that the team is not adopting. |
| `perf-issue`, `hillclimb`, `runtime-forensics`, `trace-forensics`, `visual-parity` | Specialized profiling/forensics/pixel-parity workflows deferred to keep `/develop` routing focused on daily engineering tasks. |
| `session-pickup`, `pause-safely`, `worktree-cleanup` | Operational handoff/cleanup routines tied heavily to multi-agent VM/worktree fleets (`worktree-audit.sh`). |
| `authoring-a-skill`, `eval` | Upstream skill-meta workflows tied to Cursor's built-in `/create-skill` and blinded multi-candidate eval harnesses. |

#### Omitted & consolidated principles (12 of 24)

- **Folded into kept principles or skills (3):**
  - `subtract-before-you-add` → folded into `minimize-reader-load.md` and `playbooks/refactoring.md`.
  - `attack-the-premise` → folded into `fix-root-causes.md`.
  - `encode-lessons-in-structure` → wired directly into `/develop` via `/correct`.
- **Omitted standalone principles (9):**
  - `build-the-lever`, `exhaust-the-design-space`, `experience-first`, `explain-the-number`, `make-operations-idempotent`, `migrate-callers-then-delete-legacy-apis`, `never-block-on-the-human`, `outcome-oriented-execution`, `type-system-discipline`.
  - Several core ideas remain where directly relevant (for example, migrating callers in one wave stays in `playbooks/refactoring.md`, comparing variants stays in `playbooks/prototype.md`, and proceeding on reversible work stays in `/develop`'s Autonomy section), while dropping standalone files reduces cognitive and context overhead.

#### Omitted automations, scripts & upstream scaffolding

- `automations/benny/` — Dormant Cursor Automations + Slack triage pack (Cursor-only infrastructure).
- `.cursor-plugin/`, `mirror-assets/`, `assets/`, `MIRROR.md`, `SYNC-LOG.md` — Cursor plugin and `backnotprop/pstack` mirror-sync scaffolding.
- `skills/*/agents/openai.yaml` — Codex-specific policy shims (re-add only if Codex is later adopted).
- `skills/poteto-mode/scripts/` (`watch-pr`, `worktree-audit.sh`, `bootstrap.ts`) and `skills/poteto-mode/references/bugbot-triage.md` — Supporting scripts/references for omitted `babysit`, `shipping`, and `worktree-cleanup` playbooks.
- `docs/guide/` (10 pages) and `docs/harness/claude-code.md` — Replaced by `README.md`, `AGENTS.md`, `docs/harness.md`, `docs/validation.md`, and `CHANGELOG.md`.
