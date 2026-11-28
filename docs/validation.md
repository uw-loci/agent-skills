# Installation and integration validation suite

Run this validation checklist immediately after installing skills via [AGENTS.md](../AGENTS.md), and any time after updating the repository (`git pull`) or editing `develop-config.md`.

All checks below are **read-only** against the repository and target codebase. Do not edit skills or application code while running validation; report concrete evidence and remediation steps for any failure.

---

## Expected inventory (source of truth)

- **20 skills under `skills/`:**
  `architect`, `arena`, `audit-comments`, `blast-radius`, `context`, `correct`, `create-context-guide`, `create-verification-skill`, `develop`, `how`, `in-your-own-words`, `interrogate`, `maintain-verification-skill`, `reflect`, `sharpen`, `tdd`, `teach`, `technical-writing`, `unslop`, `why`
- **7 playbooks under `skills/develop/playbooks/`:**
  `bug-fix.md`, `feature.md`, `investigation.md`, `multi-phase-plan.md`, `opening-a-pr.md`, `prototype.md`, `refactoring.md`
- **14 principles under `skills/develop/references/principles/`:**
  `accessible-by-design.md`, `boundary-discipline.md`, `fix-root-causes.md`, `foundational-thinking.md`, `guard-the-context-window.md`, `laziness-protocol.md`, `minimize-reader-load.md`, `model-the-domain.md`, `prove-it-works.md`, `redesign-from-first-principles.md`, `reproducible-immutable-artifacts.md`, `separate-before-serializing-shared-state.md`, `sequence-verifiable-units.md`, `test-behavior-not-implementation.md`
- **5 context guides under `skills/context/references/`:**
  `ecosystems/fiji-imagej.md`, `ecosystems/qupath.md`, `ecosystems/tme-quant.md`, `languages/java.md`, `languages/python.md`
- **Supporting files:**
  `skills/develop/worker.md`, `skills/develop/references/config-and-subagents.md`, `skills/audit-comments/references/comment-auditor.md`, `skills/create-verification-skill/references/feature-map-example/` (3 files: `README.md`, `create-note.md`, `search.md`), `AGENTS.md`, `CLAUDE.md`, `README.md`, `CHANGELOG.md`, `plugin.json`, `docs/harness.md`, `docs/overview.md`, `docs/quick-reference.md`, `docs/assets/architecture-overview.svg`, `docs/handouts/agent-skills-handout.pdf`, `docs/validation.md`, `scripts/build-handouts.py`, `scripts/handout-template.html`, `.github/workflows/ci.yml`

---

## Suite 1: Repository integrity checks

Run these checks against the local `uw-loci/agent-skills` clone (`<REPO>`):

1. **Skill count and frontmatter:** Confirm all 20 expected directories exist under `<REPO>/skills/`, no unexpected extra skill directories exist, and every `SKILL.md` starts with valid YAML frontmatter delimited by `---` lines whose `name:` matches its directory name and has a non-empty `description:`.
2. **Router, context, and supporting files:** Confirm `skills/develop/worker.md`, `skills/develop/references/config-and-subagents.md`, `skills/audit-comments/references/comment-auditor.md`, all 7 playbooks, all 14 principle files, all 5 context guides under `skills/context/references/`, all 3 files under `skills/create-verification-skill/references/feature-map-example/`, `CLAUDE.md`, `docs/overview.md`, `docs/quick-reference.md`, `docs/assets/architecture-overview.svg`, `docs/handouts/agent-skills-handout.pdf`, `scripts/build-handouts.py`, `scripts/handout-template.html`, and `.github/workflows/ci.yml` exist and are non-empty.
3. **No stale upstream or retired references:** Search `skills/`, `AGENTS.md`, `docs/harness.md`, `docs/overview.md`, and `docs/quick-reference.md` for leftover references that should no longer exist in operational instructions:
   - `poteto-mode`, `poteto-agent`, `comment-sicko`, `pstack-models`, `cursor-team-kit`, `/deslop`, `no-comments`, `control-ui`, `control-cli`, `principle-` (outside `CHANGELOG.md`), `.cursor/plugins`, `claude-opus-5-5`, `claude-fable-5-2`.
   - Zero hits expected across `skills/`, `AGENTS.md`, `docs/harness.md`, `docs/overview.md`, and `docs/quick-reference.md`.
4. **Developer aides parity and PDF freshness check:** Run `python "<REPO>/scripts/build-handouts.py" --check` (or `uv run --no-project python "<REPO>/scripts/build-handouts.py" --check`) to verify `docs/quick-reference.md` lists the exact 20 skills under `skills/`, `docs/assets/architecture-overview.svg` is valid XML, all relative doc links resolve, zero stale references exist, and `docs/handouts/agent-skills-handout.pdf` has 2 pages matching the current input fingerprint.

### Quick verification commands (Suite 1)

**Windows (PowerShell):**
```powershell
$repo = "<REPO>"
$errors = 0

$expectedSkills = @('architect','arena','audit-comments','blast-radius','context','correct','create-context-guide','create-verification-skill','develop','how','in-your-own-words','interrogate','maintain-verification-skill','reflect','sharpen','tdd','teach','technical-writing','unslop','why')
$actualSkills = @(Get-ChildItem -Directory "$repo\skills" | Select-Object -ExpandProperty Name | Sort-Object)
$skillDiff = Compare-Object $expectedSkills $actualSkills
if ($skillDiff) { Write-Error "Skill directory mismatch: $($skillDiff | Out-String)"; $errors++ }

foreach ($s in $expectedSkills) {
    $f = "$repo\skills\$s\SKILL.md"
    if (-not (Test-Path $f) -or (Get-Item $f).Length -eq 0) { Write-Error "Missing or empty $f"; $errors++; continue }
    $lines = Get-Content $f
    if ($lines.Count -lt 3 -or $lines[0].Trim() -ne '---') { Write-Error "Missing YAML frontmatter opening in $f"; $errors++; continue }
    $closeIdx = -1
    for ($i = 1; $i -lt $lines.Count; $i++) { if ($lines[$i].Trim() -eq '---') { $closeIdx = $i; break } }
    if ($closeIdx -lt 2) { Write-Error "Missing or empty YAML frontmatter in $f"; $errors++; continue }
    $fm = ($lines[1..($closeIdx - 1)]) -join "`n"
    if ($fm -cnotmatch "(?m)^name:[ \t]*$s[ \t]*$") { Write-Error "Frontmatter name mismatch in $f"; $errors++ }
    if ($fm -cnotmatch "(?m)^description:[ \t]*\S") { Write-Error "Missing or blank description in $f"; $errors++ }
}

$requiredFiles = @(
    'AGENTS.md',
    'CLAUDE.md',
    '.github\workflows\ci.yml',
    'docs\harness.md',
    'docs\overview.md',
    'docs\quick-reference.md',
    'docs\assets\architecture-overview.svg',
    'docs\handouts\agent-skills-handout.pdf',
    'scripts\build-handouts.py',
    'scripts\handout-template.html',
    'skills\develop\worker.md',
    'skills\develop\references\config-and-subagents.md',
    'skills\audit-comments\references\comment-auditor.md',
    'skills\create-verification-skill\references\feature-map-example\README.md',
    'skills\create-verification-skill\references\feature-map-example\create-note.md',
    'skills\create-verification-skill\references\feature-map-example\search.md'
)
foreach ($rel in $requiredFiles) {
    $p = Join-Path $repo $rel
    if (-not (Test-Path $p) -or (Get-Item $p).Length -eq 0) { Write-Error "Missing or empty $p"; $errors++ }
}

$playbooks = @(Get-ChildItem -File "$repo\skills\develop\playbooks\*.md" | Where-Object { $_.Length -gt 0 })
$principles = @(Get-ChildItem -File "$repo\skills\develop\references\principles\*.md" | Where-Object { $_.Length -gt 0 })
$contexts = @(Get-ChildItem -Recurse -File "$repo\skills\context\references\*.md" | Where-Object { $_.Length -gt 0 })
if ($playbooks.Count -ne 7) { Write-Error "Expected 7 non-empty playbooks, got $($playbooks.Count)"; $errors++ }
if ($principles.Count -ne 14) { Write-Error "Expected 14 non-empty principles, got $($principles.Count)"; $errors++ }
if ($contexts.Count -ne 5) { Write-Error "Expected 5 non-empty context guides, got $($contexts.Count)"; $errors++ }

$scanFiles = @(Get-ChildItem -Recurse -File -LiteralPath "$repo\skills","$repo\docs\harness.md","$repo\docs\overview.md","$repo\docs\quick-reference.md","$repo\AGENTS.md" -ErrorVariable gciErr | Select-Object -ExpandProperty FullName)
if ($gciErr) { Write-Error "Failed to enumerate scan targets: $gciErr"; $errors++ }
$stale = if ($scanFiles.Count -gt 0) { @(Select-String -Path $scanFiles -Pattern 'poteto-mode|poteto-agent|comment-sicko|pstack-models|cursor-team-kit|/deslop|no-comments|control-ui|control-cli|principle-|\.cursor/plugins|claude-opus-5-5|claude-fable-5-2') } else { @() }
if ($stale.Count -gt 0) { $stale | ForEach-Object { Write-Error "Stale ref: $_" }; $errors++ }

"Skills: $($actualSkills.Count)/20 | Playbooks: $($playbooks.Count)/7 | Principles: $($principles.Count)/14 | Contexts: $($contexts.Count)/5 | Stale refs: $($stale.Count) | Errors: $errors"
if ($errors -gt 0) { exit 1 }
```

**macOS / Linux (Bash):**
```bash
REPO="<REPO>"
ERRORS=0

EXPECTED_SKILLS="architect arena audit-comments blast-radius context correct create-context-guide create-verification-skill develop how in-your-own-words interrogate maintain-verification-skill reflect sharpen tdd teach technical-writing unslop why"
ACTUAL_SKILLS="$(find "$REPO/skills" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | LC_ALL=C sort | tr '\n' ' ' | sed 's/ $//')"
if [ "$ACTUAL_SKILLS" != "$EXPECTED_SKILLS" ]; then
    echo "FAIL: skill directory mismatch" >&2
    ERRORS=$((ERRORS + 1))
fi

for s in $EXPECTED_SKILLS; do
    f="$REPO/skills/$s/SKILL.md"
    if [ ! -s "$f" ]; then
        echo "FAIL: missing or empty $f" >&2
        ERRORS=$((ERRORS + 1))
        continue
    fi
    fm="$(awk '{sub(/\r$/, "")} NR==1 && $0=="---" {in_fm=1; next} in_fm && $0=="---" {closed=1; exit} in_fm {print} END {if (!closed) exit 1}' "$f")"
    if [ $? -ne 0 ]; then
        echo "FAIL: missing or unclosed YAML frontmatter in $f" >&2
        ERRORS=$((ERRORS + 1))
        continue
    fi
    if ! printf '%s\n' "$fm" | grep -qE "^name:[[:space:]]*${s}[[:space:]]*$"; then
        echo "FAIL: frontmatter name mismatch in $f" >&2
        ERRORS=$((ERRORS + 1))
    fi
    if ! printf '%s\n' "$fm" | grep -qE "^description:[[:space:]]*[^[:space:]]"; then
        echo "FAIL: missing or blank description in $f" >&2
        ERRORS=$((ERRORS + 1))
    fi
done

for rel in \
    AGENTS.md \
    CLAUDE.md \
    .github/workflows/ci.yml \
    docs/harness.md \
    docs/overview.md \
    docs/quick-reference.md \
    docs/assets/architecture-overview.svg \
    docs/handouts/agent-skills-handout.pdf \
    scripts/build-handouts.py \
    scripts/handout-template.html \
    skills/develop/worker.md \
    skills/develop/references/config-and-subagents.md \
    skills/audit-comments/references/comment-auditor.md \
    skills/create-verification-skill/references/feature-map-example/README.md \
    skills/create-verification-skill/references/feature-map-example/create-note.md \
    skills/create-verification-skill/references/feature-map-example/search.md; do
    if [ ! -s "$REPO/$rel" ]; then
        echo "FAIL: missing or empty $REPO/$rel" >&2
        ERRORS=$((ERRORS + 1))
    fi
done

PB_COUNT="$(find "$REPO/skills/develop/playbooks" -maxdepth 1 -type f -name '*.md' -size +0c | wc -l | tr -d ' ')"
PR_COUNT="$(find "$REPO/skills/develop/references/principles" -maxdepth 1 -type f -name '*.md' -size +0c | wc -l | tr -d ' ')"
CT_COUNT="$(find "$REPO/skills/context/references" -type f -name '*.md' -size +0c | wc -l | tr -d ' ')"
[ "$PB_COUNT" = "7" ] || { echo "FAIL: playbooks $PB_COUNT/7" >&2; ERRORS=$((ERRORS + 1)); }
[ "$PR_COUNT" = "14" ] || { echo "FAIL: principles $PR_COUNT/14" >&2; ERRORS=$((ERRORS + 1)); }
[ "$CT_COUNT" = "5" ] || { echo "FAIL: contexts $CT_COUNT/5" >&2; ERRORS=$((ERRORS + 1)); }

STALE_OUT="$(grep -rnE 'poteto-mode|poteto-agent|comment-sicko|pstack-models|cursor-team-kit|/deslop|no-comments|control-ui|control-cli|principle-|\.cursor/plugins|claude-opus-5-5|claude-fable-5-2' \
    "$REPO/skills" "$REPO/AGENTS.md" "$REPO/docs/harness.md" "$REPO/docs/overview.md" "$REPO/docs/quick-reference.md" 2>&1)"
GREP_RC=$?
if [ "$GREP_RC" -eq 1 ]; then
    STALE_STATUS="0"
elif [ "$GREP_RC" -eq 0 ]; then
    echo "FAIL: stale references found:" >&2
    printf '%s\n' "$STALE_OUT" >&2
    STALE_STATUS="FOUND"
    ERRORS=$((ERRORS + 1))
else
    echo "FAIL: grep error ($GREP_RC): $STALE_OUT" >&2
    STALE_STATUS="ERROR"
    ERRORS=$((ERRORS + 1))
fi

echo "Skills: $(echo "$ACTUAL_SKILLS" | wc -w | tr -d ' ')/20 | Playbooks: $PB_COUNT/7 | Principles: $PR_COUNT/14 | Contexts: $CT_COUNT/5 | Stale refs: $STALE_STATUS | Errors: $ERRORS"
[ "$ERRORS" -eq 0 ]
```

---

## Suite 2: Installation, link, and config checks

Run these checks for every coding assistant configured in `develop-config.md`:

1. **Config file exists and parses cleanly:**
   - Resolve `develop-config.md` using the base + overlay rules in [`skills/develop/references/config-and-subagents.md`](../skills/develop/references/config-and-subagents.md):
     1. User-global base: `~/.agents/develop-config.md` (with fallback to `~/.claude/rules/develop-config.md` only if `~/.agents/develop-config.md` is absent; when `install_scope` is `user-global` and Claude Code is configured, verify `~/.claude/rules/develop-config.md` exists and matches `~/.agents/develop-config.md`).
     2. Optional project-local overlay: `<target-repo>/.agents/develop-config.md` (if present, overlays keys on top of the user-global base; warn if tracked in git while holding machine-local `repo_path` or personal model preferences).
   - Verify resolved keys hold valid values:
     - `harness`: one of `antigravity`, `copilot`, `claude-code`, `cursor`, or `other` (or a comma-separated list of those values when multiple assistants share `~/.agents/develop-config.md`).
     - `repo_path`: exists on disk and contains `skills/develop/SKILL.md`.
     - `install_scope`: `user-global` or `project-local`.
     - `install_method`: `skills-json`, `symlink`, `junction`, or `copy`.
     - `delegation_policy`: `adaptive`, `single-agent`, or `always-delegate`.
     - `parallel_subagents`: integer >= `1`. *(If missing and legacy `interrogate_reviewers` or `arena_candidates` is present, verify those are integers >= `1` / >= `2` and mark **WARN** with a note to migrate to `parallel_subagents`.)*
     - `high_effort_model`, `medium_effort_model`, `low_effort_model`: each present and non-empty (`inherit` or a non-empty assistant-accepted model value; `high_effort_model` may also be a comma-separated list). *(If missing and legacy keys `code_delegate_model`, `review_model`, `research_model`, `interrogate_models`, `arena_models`, or `arena_judge_model` are present, or if `inherit-parent` or `auto` is used as a model value, mark **WARN** that legacy keys remain supported via fallback and suggest migrating to the current schema in `AGENTS.md`.)*
     - Optional `arena_cross_judge`: if present, must be `true` or `false`.
     - `default_contexts`: `auto`, `none`, or comma-separated slugs that exist in `skills/context/SKILL.md`.
2. **All 20 skills present and resolvable at the installed destination:**
   - **If `install_method` is `skills-json` (Antigravity):**
     - Verify `~/.gemini/config/skills.json` (user-global) or `<target>/.agents/skills.json` (project-local) parses as valid JSON and has an entry in `entries` whose `path` resolves to `<repo_path>/skills`.
     - On Windows, verify `path` uses an explicit forward-slash absolute path (not `~/`), and verify no ignored NTFS junctions were left behind under `~/.gemini/config/skills/` (or `<target>/.agents/skills/`).
     - Confirm all 20 skill directories, `<path>/develop/worker.md`, `<path>/develop/references/config-and-subagents.md`, `<path>/audit-comments/references/comment-auditor.md`, all 7 playbooks, all 14 principles, and all 5 context guides under `<path>/context/references/` exist and are readable at the registered `path`.
   - **If `install_method` is `symlink`, `junction`, or `copy`:**
     - For the configured assistant's destination skills directory (for example `~/.copilot/skills/`, `~/.agents/skills/`, `~/.claude/skills/`, `~/.cursor/skills/`, `~/.gemini/config/skills/` for static copies, or the project-local equivalent):
       - Confirm all 20 skill directories exist and `<dest>/<skill>/SKILL.md` is readable.
       - Confirm `<dest>/develop/worker.md`, `<dest>/develop/references/config-and-subagents.md`, `<dest>/audit-comments/references/comment-auditor.md`, all 7 playbooks, all 14 principles, and all 5 context guides under `<dest>/context/references/` are readable through the installed link.
       - If `install_method` is `symlink` or `junction`, verify every skill entry is actually a link pointing inside `repo_path` (not a broken link or stale orphaned directory).
3. **Claude Code rule link and optional custom agent wrappers (when configured):**
   - **Claude Code (user-global):** Verify `~/.claude/rules/develop-config.md` resolves cleanly and matches `~/.agents/develop-config.md`.
   - **Optional custom agent wrappers (any assistant):** Separate custom agent files are not shipped by this kit. Skip agent-file checks unless the user created optional local wrappers per Section 3 of [docs/harness.md](harness.md).
4. **Skills remain immutable:** Run `git -C "<repo_path>" status --short skills/` and confirm installation did not modify any tracked skill files.

---

## Suite 3: Live integration and smoke tests

Run these behavioral smoke checks inside the installed coding assistant (open a **new chat session** first if skills were just linked so the catalog reloads):

1. **Catalog discovery check:**
   - Confirm the assistant lists `develop`, `context`, and the 18 sibling skills in its active skill catalog or `/` menu. *(Note: 19 of the 20 skills set `disable-model-invocation: true`, so in assistants like Antigravity only `context` appears in the model's auto-discovery `<skills>` list while all 20 are exposed as manual `/` slash commands.)*
   - *Pass criterion:* All 20 skill names are discoverable without naming errors.
2. **Config resolution check:**
   - Read the active `develop-config.md` files following the base + overlay chain and print the resolved values for `harness`, `delegation_policy`, `parallel_subagents`, `high_effort_model`, `medium_effort_model`, `low_effort_model`, and `default_contexts` (plus `arena_cross_judge` or any active legacy fallback keys).
   - *Pass criterion:* Resolved values match what the user chose during installation.
3. **Router, playbook, and principle smoke test (read-only):**
   - Trace the `/develop` skill on a synthetic read-only question (*"How does configuration resolution work in this kit? Read-only check."*):
     - Read `<installed>/develop/SKILL.md` and `<installed>/develop/references/config-and-subagents.md`
     - Confirm it matches `playbooks/investigation.md` and read that file
     - Read one principle file (`references/principles/prove-it-works.md`) and cite one concrete rule from it
   - *Pass criterion:* All four files resolve cleanly through the installed path and the agent makes zero file edits.
4. **Cross-skill wiring check:**
   - Verify sibling references resolve from the installed skills directory (all 15 chains):
     - `develop` to `context`, `references/config-and-subagents.md`, `architect`, `arena`, `audit-comments`, `interrogate`, `blast-radius`, `unslop`, `technical-writing`, `create-verification-skill`, `correct`, `tdd`, `how`, `why`
     - `context` to all 5 reference guides (`ecosystems/fiji-imagej.md`, `ecosystems/tme-quant.md`, `ecosystems/qupath.md`, `languages/java.md`, `languages/python.md`), `create-context-guide`, and `develop/references/config-and-subagents.md`
     - `create-context-guide` to `context`, `unslop`, and `develop/references/config-and-subagents.md`
     - `architect` to `arena` and `develop/references/config-and-subagents.md`
     - `arena` to `develop/references/config-and-subagents.md` and `develop/references/principles/`
     - `audit-comments` to `references/comment-auditor.md`, `develop/references/config-and-subagents.md`, `why`, `architect`, and `develop/references/principles/`
     - `blast-radius` to `arena`, `how`, `why`, `unslop`, and `develop/references/config-and-subagents.md`
     - `interrogate` to `in-your-own-words`, `develop/references/config-and-subagents.md`, and `develop/references/principles/`
     - `tdd` to `develop/references/principles/test-behavior-not-implementation.md`
     - `how` to `develop/references/config-and-subagents.md`
     - `teach` to `how`, `why`, `unslop`, and `develop/references/config-and-subagents.md`
     - `technical-writing` to `unslop`
     - `create-verification-skill` to `maintain-verification-skill` and `references/feature-map-example/`
     - `maintain-verification-skill` to `create-verification-skill` and `develop/references/config-and-subagents.md`
     - `reflect` to `correct` and `develop/references/config-and-subagents.md`
   - *Pass criterion:* Every referenced sibling `SKILL.md` and local reference file exists and is readable at the installed path.
5. **Subagent and configured-model verification:**
   - Collect every distinct model value configured across `high_effort_model`, `medium_effort_model`, and `low_effort_model` (splitting comma-separated lists and including any active legacy per-skill model keys). Treat `inherit-parent` and `auto` as `inherit`.
   - **If your coding assistant has no subagent tool:** Mark **SKIP** when all models are `inherit`, or **WARN** when non-`inherit` models are configured because model overrides cannot run without subagents.
   - **If one or more non-`inherit` model values are configured (run even when `delegation_policy` is `single-agent`, because explicit multi-agent skills still spawn subagents with these models):**
     - For **each distinct non-`inherit` model value**, spawn one lightweight read-only subagent using that configured model value (splitting `<model> <effort>` into separate `model` and `effort` parameters when supported by your assistant's subagent tool; see [`skills/develop/references/config-and-subagents.md`](../skills/develop/references/config-and-subagents.md)), with first line `Read <installed>/develop/worker.md before anything else.`, asking it to return the exact text of the second bullet in `worker.md`. Distinct models may be tested concurrently.
     - Record each tested model value and its outcome (`PASS` or `FAIL`) in the validation report.
     - *Pass criterion:* Every distinct configured model spawns without a model-rejection or unsupported-model error, reads `worker.md`, and returns the accurate second bullet text.
     - *Failure remediation:* If any configured model fails or is rejected, mark **FAIL**, name the offending config keys and rejected values, list the valid model values accepted by this assistant's subagent tool (see [`skills/develop/references/config-and-subagents.md`](../skills/develop/references/config-and-subagents.md)), and guide the user to update `develop-config.md` and re-run Suite 3 Check 5 until every configured model passes.
   - **If all configured models are `inherit`:**
     - If `delegation_policy` is `single-agent`, mark **SKIP** (or run one `inherit` check if the user plans to invoke multi-agent skills).
     - Otherwise, spawn one lightweight read-only subagent omitting the model override (`inherit`), with first line `Read <installed>/develop/worker.md before anything else.`, asking it to return the exact text of the second bullet in `worker.md`.
     - *Pass criterion:* Subagent spawns cleanly, reads `worker.md`, and returns the accurate line.

---

## Report format

Present results in a concise table before declaring installation or validation complete:

| Suite | Check | Status | Evidence / Notes |
|---|---|---|---|
| 1. Repo | 20 skills and frontmatter | PASS / FAIL | Example: `20/20 skills valid` |
| 1. Repo | Playbooks (7), Principles (14), Contexts (5), Support files | PASS / FAIL | Example: `7/7, 14/14, 5/5, support OK` |
| 1. Repo | Zero stale upstream or retired references | PASS / FAIL | Example: `0 hits` |
| 1. Repo | Developer aides parity and 2-page PDF | PASS / FAIL | `scripts/build-handouts.py --check` (`20/20`, valid SVG, 2 pages) |
| 2. Install | `develop-config.md` valid and resolved | PASS / WARN / FAIL | path, `harness`, policy, `parallel_subagents`, effort-tier models, contexts |
| 2. Install | 20 skill links intact and immutable | PASS / FAIL | destination path, link count, clean `git status` |
| 2. Install | Claude Code rule link (if applicable) | PASS / WARN / SKIP | Example: Claude rules symlink verified |
| 3. Live | Assistant catalog discovery | PASS / WARN | note if a fresh chat or reload is needed |
| 3. Live | Router, playbook, config, and principle dry run | PASS / FAIL | files read through installed path |
| 3. Live | Cross-skill and context guide wiring | PASS / FAIL | all 15 dependency chains verified |
| 3. Live | Subagent and configured-model verification | PASS / WARN / FAIL / SKIP | every distinct configured model tested and confirmed output |

## Common failures and fixes

- **Catalog does not show newly linked skills:** Start a new chat session or reload the IDE window; coding assistants typically scan skill directories at session start.
- **Antigravity on Windows does not show skills in `/` menu:** Antigravity's Windows directory walker skips NTFS directory junctions under `~/.gemini/config/skills/`, and does not expand `~/` in `skills.json`. Remove any junctions under `~/.gemini/config/skills/` and register `"path": "C:/.../skills"` (explicit forward-slash absolute path) in `~/.gemini/config/skills.json` (or `<target>/.agents/skills.json`), with `install_method: skills-json` in `develop-config.md`.
- **Windows `SymbolicLink` permission denied (non-Antigravity assistants):** Switch `install_method` to `junction` and link directories with `New-Item -ItemType Junction` (or `mklink /J`), which requires no elevation.
- **Configured model rejected or deprecated by subagent tool:** Check which values your assistant's subagent tool accepts in [`skills/develop/references/config-and-subagents.md`](../skills/develop/references/config-and-subagents.md) (for example, Antigravity's `invoke_subagent` accepts only `inherit`, `pro`, `flash`, and `flash_lite`, not individual model names). Update the offending key in `develop-config.md` to a supported value or `inherit`, then re-run Suite 3 Check 5.
- **Broken links or paths after moving the local clone:** Update `repo_path` in `develop-config.md` and update `skills.json` (if `install_method: skills-json`) or re-run Step 3 of [AGENTS.md](../AGENTS.md).
