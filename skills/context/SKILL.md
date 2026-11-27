---
name: context
description: "Loads and configures UW-LOCI multi-repo development context guides (Fiji/ImageJ/SciJava, TME-Quant/CurveAlign, QuPath extensions) and team Java/Python conventions on demand. Use automatically when working in a matching repository or language, or explicitly via /context, /context <name>, or /context configure."
---

# Development context guides

Load **only** the guide or guides matching the active repository, org, or language so unrelated ecosystem maps stay out of the context window.

Check `default_contexts` in `develop-config.md` (`.agents/develop-config.md`, `~/.claude/rules/develop-config.md`, or `~/.agents/develop-config.md`):
- `auto` (default): match the active repo and language using the tables below.
- Comma-separated slugs (for example, `tme-quant, python`): load those exact guides automatically.
- `none`: load guides only when the user requests `/context <name>`.

## Ecosystem guides

| Slug | Guide | Triggers (orgs, repos, topics) | Companion guides |
|---|---|---|---|
| `fiji-imagej` | [`references/ecosystems/fiji-imagej.md`](references/ecosystems/fiji-imagej.md) | `scijava/*`, `imglib/*`, `scifio/*`, `imagej/*`, `fiji/*`, `apposed/*`, `pom-scijava`, Fiji update sites, ImageJ2, ImgLib2, SCIFIO, PyImageJ, ScyJava, Appose, Jaunch, jgo, SciJava Ops, `scikit-ops` | `java` (plus `python` for PyImageJ, ScyJava, Appose, or `scikit-ops`) |
| `tme-quant` | [`references/ecosystems/tme-quant.md`](references/ecosystems/tme-quant.md) | `uw-loci/tme-quant`, `uw-loci/fiji-curvealign`, `uw-loci/napari-curvealign`, `uw-loci/curvelets`, CurveAlign, CT-FIRE, `pycurvelets`, `curvelops` | `python` (plus `java` and `fiji-imagej` for `fiji-curvealign`) |
| `qupath` | [`references/ecosystems/qupath.md`](references/ecosystems/qupath.md) | `uw-loci/qupath-*`, `qupath/qupath`, QP-CAT, QuIET, QuPath extensions | `python` (when Appose Python workers are involved) |

## Language guides

| Slug | Guide | Triggers |
|---|---|---|
| `java` | [`references/languages/java.md`](references/languages/java.md) | Java and Maven repos across UW-LOCI, SciJava, ImageJ, Fiji, ImgLib2, SCIFIO (`pom.xml`, `.java`) |
| `python` | [`references/languages/python.md`](references/languages/python.md) | Python and `uv` repos across UW-LOCI (`pyproject.toml`, `.py`, `pytest`, `ruff`, `napari`, `pyimagej`, `appose-python`) |

## Configuring default guides (`/context configure`)

Run this interactive flow when the user invokes `/context configure`, asks to list or change active guides, or picks "Choose specific guides now" during installation (`AGENTS.md` Question 7).

1. **Read the live catalog.** Build the list of choices from the **Ecosystem guides** and **Language guides** tables above rather than from memory so guides added later appear automatically.
2. **Resolve scope and mode (standalone runs only).** Skip this step when called from `AGENTS.md` Question 7, because scope and mode are already chosen there. Otherwise:
   - Read the active `develop-config.md` (`.agents/develop-config.md`, `~/.claude/rules/develop-config.md`, or `~/.agents/develop-config.md`) and report its path and current `default_contexts` value.
   - If the active workspace is a repository without `.agents/develop-config.md`, ask whether to update the user-global config or create a project-local `.agents/develop-config.md` override.
   - Ask whether `default_contexts` should be `auto`, specific guides chosen from the catalog, or `none`.
3. **Run the interactive guide picker (when choosing specific guides).**
   - Present every guide from the tables above with its slug, category (`Ecosystem` or `Language`), and a concise summary of what it covers. Mark any slugs that are currently active when reconfiguring.
   - Use the assistant's native multi-select checkbox UI when available (see `docs/harness.md`, such as `ask_question` with `is_multi_select: true` in Antigravity or `AskUserQuestion` with `multiSelect: true` in Claude Code).
   - If all guides fit in one multi-select prompt for the active assistant, show a single checklist with labels in the form `<slug> (Ecosystem): <short summary>` or `<slug> (Language): <short summary>`.
   - If the assistant caps options per question (such as 4 options per question in Claude Code) or the catalog grows large, split into two multi-select questions (**Ecosystem guides** and **Language guides**, each with a `None` option) or present a numbered list in chat so the user can reply with numbers such as `1, 4`.
   - Note companion pairings from the **Companion guides** column above in one line, while allowing any combination.
   - If the user selects zero guides (or only `None`), confirm whether to save `default_contexts: none` or `default_contexts: auto`.
4. **Save `default_contexts` without modifying `skills/`.**
   - Write the chosen value (`auto`, `none`, or comma-separated slugs in table order) to `default_contexts:` in the target `develop-config.md`.
   - When creating a new project-local `.agents/develop-config.md` and a user-global `~/.agents/develop-config.md` exists, copy the user-global config first and change only `default_contexts:` so other settings (`delegation_policy`, `parallel_subagents`, model tiers, `install_scope`) stay intact.
   - If no `develop-config.md` exists yet (and this is not part of installation), tell the user to run the `AGENTS.md` installation flow or create the target file using the schema in `AGENTS.md`.
   - When updating user-global `~/.agents/develop-config.md` and `~/.claude/rules/develop-config.md` exists as a static copy (not a symlink), update that copy too.
   - Report the updated config path and `default_contexts` value. Mention `/create-context-guide` if the user needs a guide for a stack not listed.

## Adding or updating a guide

Use [`/create-context-guide`](../create-context-guide/SKILL.md) to add a new team ecosystem or language guide and register it in the tables above.
