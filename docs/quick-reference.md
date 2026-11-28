# Quick reference

All 20 `/` commands exposed after installing `uw-loci/agent-skills`. For how the pieces fit together, see [How uw-loci/agent-skills works](overview.md). For the double-sided printable version, open [agent-skills-handout.pdf](handouts/agent-skills-handout.pdf).

**How to use any command:** Type `/<command>` followed by your target. Unsure what to pass? Check its `/` menu tooltip, or run the command alone so the assistant asks for details (or defaults to your current branch diff) before editing files.

**Tags:** `diff` defaults to current branch diff · `pauses` waits for your approval before editing · `subagents` spawns helper agents · `auto` runs automatically on matching repos.

## Everyday 5 (start here)

Most daily work uses these five commands. Ignore the other 15 until you need them.

| Command | Use when | Input and tags |
|---|---|---|
| `/develop` | Bugs, features, refactors, plans, prototypes, or PRs | Goal + done check + constraints (or run alone) |
| `/how` | Trace how a subsystem works or where code belongs | Subsystem, file, or question (`subagents`) |
| `/tdd` | Write a failing test first, confirm it fails, then fix it | Bug or expected behavior |
| `/interrogate` | Adversarial review where only run-proven bugs survive | Target or branch diff (`diff`, `subagents`) |
| `/context` | Load or configure UW-LOCI repo maps and Java or Python guides | Alone, `<slug>`, or `configure` (`auto`) |

## All other 15 commands

### Understand

| Command | Use when | Tags |
|---|---|---|
| `/why` | Trace design rationale from git commits and PR discussions | |
| `/teach` | Plain-language, step-by-step walkthrough with diagrams | |

### Frame and design

| Command | Use when | Tags |
|---|---|---|
| `/in-your-own-words` | Have the agent restate your goal before editing anything | `pauses` |
| `/sharpen` | Rewrite a rough prompt for rigor without running it | `pauses` |
| `/architect` | Compare two structural designs across types or boundaries | `pauses` |
| `/blast-radius` | Find hidden downstream breakage and prove the core safety fact | `diff` |
| `/arena` | Run parallel independent attempts on a hard task and merge the best parts | `subagents` |

### Verify and maintain

| Command | Use when | Tags |
|---|---|---|
| `/create-verification-skill` | Generate a repo-local `verify-<app>` end-to-end test skill and prove it once | |
| `/maintain-verification-skill` | Audit and run an existing repo `verify-<app>` skill against live code | `subagents` |

### Clean and write

| Command | Use when | Tags |
|---|---|---|
| `/audit-comments` | Audit comments and lint or type suppressions for clutter or hidden bugs | `diff`, `pauses`, `subagents` |
| `/unslop` | Strip AI filler, buzzwords, and vague wording from prose | |
| `/technical-writing` | Write or edit docs, READMEs, RFCs, PR descriptions, or commit messages | |

### Context and team learning

| Command | Use when | Tags |
|---|---|---|
| `/create-context-guide` | Add or update a team repo map or language convention guide | `pauses` |
| `/correct` | Turn repeat agent mistakes into permanent code, type, lint, or test checks | `pauses` |
| `/reflect` | Propose targeted edits to existing skills from lessons in this session | `pauses` |

## Settings (`develop-config.md`)

Edit `~/.agents/develop-config.md` (global base) or `<repo>/.agents/develop-config.md` (optional per-repo overlay). Changes take effect without touching `skills/`.

| Key | Default and options |
|---|---|
| `delegation_policy` | `adaptive` (default), `single-agent` (no helper subagents), or `always-delegate` |
| `parallel_subagents` | `2` (default; `1` to `3` fan-out for `/interrogate`, `/arena`, `/maintain-verification-skill`) |
| `high`, `medium`, `low_effort_model` | `inherit` (default; reuses active chat model) or assistant-accepted model values |
| `default_contexts` | `auto` (default), `none`, or pinned slugs (change interactively with `/context configure`) |

For supported model values per coding assistant and fallback rules, see [config-and-subagents.md](../skills/develop/references/config-and-subagents.md).
