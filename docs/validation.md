# Installation & Integration Validation Suite

Run this validation checklist immediately after installing skills via [AGENTS.md](../AGENTS.md), and any time after updating the repository (`git pull`) or editing `develop-config.md`.

All checks below are **read-only** against the repository and target codebase. Do not edit skills or application code while running validation; report concrete evidence and remediation steps for any failure.

---

## Expected inventory (source of truth)

- **20 skills under `skills/`:**
  `architect`, `arena`, `blast-radius`, `context`, `correct`, `create-context-guide`, `create-verification-skill`, `develop`, `how`, `in-your-own-words`, `interrogate`, `maintain-verification-skill`, `no-comments`, `reflect`, `sharpen`, `tdd`, `teach`, `technical-writing`, `unslop`, `why`
- **7 playbooks under `skills/develop/playbooks/`:**
  `bug-fix.md`, `feature.md`, `investigation.md`, `multi-phase-plan.md`, `opening-a-pr.md`, `prototype.md`, `refactoring.md`
- **12 principles under `skills/develop/references/principles/`:**
  `boundary-discipline.md`, `fix-root-causes.md`, `foundational-thinking.md`, `guard-the-context-window.md`, `laziness-protocol.md`, `minimize-reader-load.md`, `model-the-domain.md`, `prove-it-works.md`, `redesign-from-first-principles.md`, `separate-before-serializing-shared-state.md`, `sequence-verifiable-units.md`, `test-behavior-not-implementation.md`
- **5 context guides under `skills/context/references/`:**
  `ecosystems/fiji-imagej.md`, `ecosystems/qupath.md`, `ecosystems/tme-quant.md`, `languages/java.md`, `languages/python.md`
- **2 agent definitions under `agents/`:**
  `develop-agent.md`, `comment-auditor.md` (with `skills/no-comments/references/comment-auditor.md` byte-identical to `agents/comment-auditor.md`)
- **Supporting files:**
  `skills/develop/worker.md`, `skills/create-verification-skill/references/feature-map-example/` (3 files), `AGENTS.md`, `README.md`, `CHANGELOG.md`, `plugin.json`, `docs/harness.md`, `docs/validation.md`

---

## Suite 1: Repository integrity checks

Run these checks against the local `uw-loci/pstack` clone (`<REPO>`):

1. **Skill count & frontmatter:** Confirm all 20 expected directories exist under `<REPO>/skills/`, no unexpected extra skill directories exist, and every `SKILL.md` starts with YAML frontmatter whose `name:` matches its directory name and has a non-empty `description:`.
2. **Router & context internals:** Confirm `skills/develop/worker.md`, all 7 playbooks, all 12 principle reference files, and all 5 context guides under `skills/context/references/` exist and are non-empty.
3. **Agent parity:** Confirm `agents/develop-agent.md` and `agents/comment-auditor.md` exist, and `skills/no-comments/references/comment-auditor.md` matches `agents/comment-auditor.md` identically.
4. **No stale upstream references:** Search `skills/`, `agents/`, `AGENTS.md`, and `docs/` for leftover references that should no longer exist in operational instructions:
   - `poteto-mode`, `poteto-agent`, `comment-sicko`, `pstack-models`, `cursor-team-kit`, `/deslop`, `control-ui`, `control-cli`, `principle-` (outside `CHANGELOG.md`), `.cursor/skills`, `claude-opus-5-5`, `claude-fable-5-2`.
   - Zero hits expected across `skills/`, `agents/`, `AGENTS.md`, and `docs/harness.md`.

### Quick verification commands (Suite 1)

**Windows (PowerShell):**
```powershell
$repo = "<REPO>"
$expectedSkills = @('architect','arena','blast-radius','context','correct','create-context-guide','create-verification-skill','develop','how','in-your-own-words','interrogate','maintain-verification-skill','no-comments','reflect','sharpen','tdd','teach','technical-writing','unslop','why')
$actualSkills = (Get-ChildItem -Directory "$repo\skills" | Select-Object -ExpandProperty Name | Sort-Object)
Compare-Object $expectedSkills $actualSkills

foreach ($s in $expectedSkills) {
    $f = "$repo\skills\$s\SKILL.md"
    if (-not (Test-Path $f)) { Write-Error "Missing $f"; continue }
    $head = (Get-Content $f -TotalCount 10) -join "`n"
    if ($head -notmatch "(?m)^name:\s*$s\s*$") { Write-Error "Frontmatter name mismatch in $f" }
    if ($head -notmatch "(?m)^description:\s*.+") { Write-Error "Missing description in $f" }
}

$playbooks = (Get-ChildItem -File "$repo\skills\develop\playbooks\*.md").Count
$principles = (Get-ChildItem -File "$repo\skills\develop\references\principles\*.md").Count
$contexts = (Get-ChildItem -Recurse -File "$repo\skills\context\references\*.md").Count
$sameAuditor = (Get-FileHash "$repo\agents\comment-auditor.md").Hash -eq (Get-FileHash "$repo\skills\no-comments\references\comment-auditor.md").Hash
"Skills: $($actualSkills.Count)/20 | Playbooks: $playbooks/7 | Principles: $principles/12 | Contexts: $contexts/5 | Auditor parity: $sameAuditor"

Select-String -Path (Get-ChildItem -Recurse -File "$repo\skills","$repo\agents","$repo\docs\harness.md","$repo\AGENTS.md" | Select-Object -ExpandProperty FullName) -Pattern 'poteto-mode|poteto-agent|comment-sicko|pstack-models|cursor-team-kit|/deslop|control-ui|control-cli|\.cursor/|claude-opus-5-5|claude-fable-5-2'
```

**macOS / Linux (Bash):**
```bash
REPO="<REPO>"
echo "Skills: $(find "$REPO/skills" -mindepth 1 -maxdepth 1 -type d | wc -l)/20"
echo "Playbooks: $(find "$REPO/skills/develop/playbooks" -maxdepth 1 -name '*.md' | wc -l)/7"
echo "Principles: $(find "$REPO/skills/develop/references/principles" -maxdepth 1 -name '*.md' | wc -l)/12"
echo "Contexts: $(find "$REPO/skills/context/references" -type f -name '*.md' | wc -l)/5"
diff -q "$REPO/agents/comment-auditor.md" "$REPO/skills/no-comments/references/comment-auditor.md" && echo "Auditor parity: OK"
grep -rnE 'poteto-mode|poteto-agent|comment-sicko|pstack-models|cursor-team-kit|/deslop|control-ui|control-cli|\.cursor/|claude-opus-5-5|claude-fable-5-2' \
  "$REPO/skills" "$REPO/agents" "$REPO/AGENTS.md" "$REPO/docs/harness.md" || echo "Stale refs: 0"
```

---

## Suite 2: Installation, link & config checks

Run these checks for every harness configured in `develop-config.md`:

1. **Config file exists and parses cleanly:**
   - Locate `develop-config.md` using the priority order:
     1. `<target-repo>/.agents/develop-config.md` (if project-local)
     2. `~/.claude/rules/develop-config.md` (if Claude Code is configured — verify it exists and resolves to the same content as `~/.agents/develop-config.md`)
     3. `~/.agents/develop-config.md`
   - Verify required keys exist and hold valid values:
     - `repo_path`: exists on disk and contains `skills/develop/SKILL.md`.
     - `install_scope`: `user-global` or `project-local`.
     - `install_method`: `symlink`, `junction`, or `copy`.
     - `delegation_policy`: `adaptive`, `single-agent`, or `always-delegate`.
     - `interrogate_reviewers`: integer >= `1`.
     - `arena_candidates`: integer >= `2`.
     - `arena_cross_judge`: `true` or `false`.
     - `default_contexts`: `auto`, `none`, or comma-separated slugs that exist in `skills/context/SKILL.md`.
2. **All 20 skills present and resolvable at the installed destination:**
   - For each configured harness's destination skills directory (`~/.gemini/config/skills/`, `~/.copilot/skills/`, `~/.agents/skills/`, `~/.claude/skills/`, or the project-local equivalent):
     - Confirm all 20 skill directories exist and `<dest>/<skill>/SKILL.md` is readable.
     - Confirm `<dest>/develop/worker.md`, all 7 playbooks, all 12 principles, and all 5 context guides under `<dest>/context/references/` are readable *through the installed link*.
     - If `install_method` is `symlink` or `junction`, verify every skill entry is actually a link pointing inside `repo_path` (not a broken link or stale orphaned directory).
3. **Harness-specific agent links (when configured):**
   - **Claude Code:** Verify `~/.claude/agents/develop-agent.md` and `comment-auditor.md` (or project-local `.claude/agents/`) resolve cleanly.
   - **VS Code / GitHub Copilot (optional):** If `.agent.md` wrappers were installed under `~/.copilot/agents/` or `.github/agents/`, verify they are readable and contain valid frontmatter.
4. **Skills remain immutable:** Run `git -C "<repo_path>" status --short skills/ agents/` and confirm installation did not modify any tracked skill files.

---

## Suite 3: Live integration & smoke tests

Run these behavioral smoke checks inside the installed harness (open a **new chat session** first if skills were just linked so the catalog reloads):

1. **Catalog discovery check:**
   - Confirm the harness lists `develop`, `context`, and the 18 sibling skills in its active skill catalog or `/` menu.
   - *Pass criterion:* All 20 skill names are discoverable without naming errors.
2. **Config resolution check:**
   - Read the active `develop-config.md` following the priority chain and print the resolved values for `delegation_policy`, `code_delegate_model`, `review_model`, `research_model`, `interrogate_reviewers`, `arena_candidates`, `arena_cross_judge`, and `default_contexts`.
   - *Pass criterion:* Resolved values match what the user chose during installation.
3. **Router + playbook + principle smoke test (read-only):**
   - Trace the `/develop` skill on a synthetic read-only question (*"How does configuration resolution work in this kit? Read-only check."*):
     - Read `<installed>/develop/SKILL.md`
     - Confirm it matches `playbooks/investigation.md` and read that file
     - Read one principle file (`references/principles/prove-it-works.md`) and cite one concrete rule from it
   - *Pass criterion:* All three files resolve cleanly through the installed path and the agent makes zero file edits.
4. **Cross-skill wiring check:**
   - Verify sibling references resolve from the installed skills directory:
     - `develop` -> `context`
     - `context` -> all 5 reference guides (`ecosystems/fiji-imagej.md`, `ecosystems/tme-quant.md`, `ecosystems/qupath.md`, `languages/java.md`, `languages/python.md`) and `create-context-guide`
     - `architect` -> `arena`
     - `blast-radius` -> `arena`, `how`, `why`, `unslop`
     - `teach` -> `how`, `why`, `unslop`
     - `technical-writing` -> `unslop`
     - `no-comments` -> `references/comment-auditor.md`, `why`, `architect`
     - `create-verification-skill` -> `maintain-verification-skill`
   - *Pass criterion:* Every referenced sibling `SKILL.md` and local reference file exists and is readable at the installed path.
5. **Subagent & model-parameter smoke test (skip if `delegation_policy: single-agent` or harness has no subagent tool):**
   - Spawn one lightweight read-only subagent using the configured `research_model` (omitting the model override when set to `inherit-parent`), with first line `Read <installed>/develop/worker.md before anything else.`, asking it to return the exact text of the second bullet in `worker.md`.
   - *Pass criterion:* Subagent spawns without a model-rejection error, reads `worker.md`, and returns the accurate line. (If the harness rejects a configured model slug, mark **FAIL** and guide the user to update `develop-config.md` to a valid tier or `inherit-parent`.)

---

## Report format

Present results in a concise table before declaring installation or validation complete:

| Suite | Check | Status | Evidence / Notes |
|---|---|---|---|
| 1. Repo | 20 skills & frontmatter | PASS / FAIL | e.g., `20/20 skills valid` |
| 1. Repo | Playbooks (7), Principles (12), Contexts (5), Auditor parity | PASS / FAIL | e.g., `7/7, 12/12, 5/5, hash match` |
| 1. Repo | Zero stale upstream references | PASS / FAIL | e.g., `0 hits` |
| 2. Install | `develop-config.md` valid & resolved | PASS / FAIL | path + active policy/panel counts/contexts |
| 2. Install | 20 skill links intact & immutable | PASS / FAIL | destination path + link count + clean `git status` |
| 2. Install | Harness agent/rule links (if applicable) | PASS / WARN / SKIP | e.g., Claude rules symlink verified |
| 3. Live | Harness catalog discovery | PASS / WARN | note if a fresh chat/reload is needed |
| 3. Live | Router + playbook + principle dry run | PASS / FAIL | files read through installed path |
| 3. Live | Cross-skill & context guide wiring | PASS / FAIL | all 8 dependency chains verified |
| 3. Live | Subagent + model config smoke test | PASS / FAIL / SKIP | model used + confirmed output |

## Common failures & fixes

- **Catalog does not show newly linked skills:** Start a new chat session or reload the IDE window; harnesses typically scan skill directories at session start.
- **Windows `SymbolicLink` permission denied:** Switch `install_method` to `junction` and link directories with `New-Item -ItemType Junction` (or `mklink /J`), which requires no elevation.
- **Model slug rejected by subagent tool:** Open `develop-config.md` and change the offending key to `inherit-parent` or a harness-supported tier from [docs/harness.md](harness.md).
- **Broken links after moving the local clone:** Update `repo_path` in `develop-config.md` and re-run Step 3 of [AGENTS.md](../AGENTS.md).
