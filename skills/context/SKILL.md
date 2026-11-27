---
name: context
description: "Load or configure UW-LOCI multi-repo ecosystem guides (Fiji/ImageJ/SciJava, TME-Quant/CurveAlign, QuPath extensions) and Java/Python conventions on demand. Auto-loads matching guides in supported repos, or run /context (auto-load or list guides), /context <slug>, or /context configure."
---

# Development context guides

Load **only** the guide or guides matching the active repository, organization, or language (unless the user explicitly pinned specific slugs in `default_contexts`) so unrelated repo maps stay out of the context window.

Resolve `default_contexts` from `develop-config.md` per [`../develop/references/config-and-subagents.md`](../develop/references/config-and-subagents.md) (default `auto`):

- `auto`: match the active repository and language using the tables below.
- Comma-separated slugs (for example, `tme-quant, python`): override auto-detection and load those exact guides automatically.
- `none`: load guides only when the user requests `/context <slug>`.

## Handling explicit `/context` invocations

- **`/context` (no arguments):** Report the active `default_contexts` setting and which guides match the current workspace.
  - If `default_contexts` is `auto` and guides match, load those matching guides now.
  - If `default_contexts` specifies comma-separated slugs, load those configured guides now.
  - Otherwise (no match under `auto`, or `default_contexts: none`), list the available slugs from the tables below and mention `/context <slug>` (to load one for this session) and `/context configure` (to change saved defaults).
- **`/context <slug>`:** Read the matching reference file from the tables below immediately (even if `default_contexts` is `none`). Also load any companion guide listed in its **Companion guides** column when the active workspace uses that language or stack. If `<slug>` is unknown, list the valid slugs from the tables below.
- **`/context configure`:** Run the interactive flow in `Configuring default guides` below.

## Ecosystem guides

| Slug | Guide | Triggers (orgs, repos, topics) | Companion guides |
|---|---|---|---|
| `fiji-imagej` | [`references/ecosystems/fiji-imagej.md`](references/ecosystems/fiji-imagej.md) | `scijava/*`, `imglib/*`, `scifio/*`, `imagej/*`, `fiji/*`, `apposed/*`, `pom-scijava`, Fiji update sites, ImageJ2, ImgLib2, SCIFIO, PyImageJ, ScyJava, Appose, Jaunch, jgo, SciJava Ops, `scikit-ops` | `java` (plus `python` for PyImageJ, ScyJava, Appose, or `scikit-ops`) |
| `tme-quant` | [`references/ecosystems/tme-quant.md`](references/ecosystems/tme-quant.md) | `uw-loci/tme-quant`, `uw-loci/fiji-curvealign`, `uw-loci/napari-curvealign`, `uw-loci/curvelets`, CurveAlign, CT-FIRE, `pycurvelets`, `curvelops` | `python` (plus `java` and `fiji-imagej` for `fiji-curvealign`) |
| `qupath` | [`references/ecosystems/qupath.md`](references/ecosystems/qupath.md) *(starter draft)* | `uw-loci/qupath-*`, `qupath/qupath`, QP-CAT, QuIET, QuPath extensions | `python` (when Appose Python workers are involved) |

## Language guides

| Slug | Guide | Triggers |
|---|---|---|
| `java` | [`references/languages/java.md`](references/languages/java.md) | Java and Maven repos across UW-LOCI, SciJava, ImageJ, Fiji, ImgLib2, SCIFIO (`pom.xml`, `.java`) |
| `python` | [`references/languages/python.md`](references/languages/python.md) | Python and `uv` repos across UW-LOCI (`pyproject.toml`, `.py`, `pytest`, `ruff`, `napari`, `pyimagej`, `appose-python`) |

## Configuring default guides (`/context configure`)

Run this interactive flow when the user invokes `/context configure`, asks to list or change active guides, or picks "Choose specific guides now" during installation.

1. **Read the live catalog.** Build the list of choices from the **Ecosystem guides** and **Language guides** tables above rather than from memory so guides added later appear automatically. Preserve any status label such as `(starter draft)`.
2. **Resolve scope and mode (standalone runs only).** Skip this step when called during initial installation, because scope and mode are already chosen there. Otherwise:
   - Read the active `develop-config.md` files per `../develop/references/config-and-subagents.md` and report their paths and resolved `default_contexts` value.
   - If the active workspace is a repository, ask whether to update the user-global config (`~/.agents/develop-config.md`) or create/update the project-local `.agents/develop-config.md` override. If `.agents/develop-config.md` already exists, explicitly note whether it currently overrides the global setting and whether it is tracked in git before editing it.
   - Ask whether `default_contexts` should be `auto`, specific guides chosen from the catalog, or `none`.
3. **Run the interactive guide picker (when choosing specific guides).**
   - Present every guide from the tables above with its slug, category (`Ecosystem` or `Language`), status note if any, and a short summary of what it covers. Mark any slugs that are currently active when reconfiguring.
   - Use the assistant's native multi-select checkbox UI when available (see `../develop/references/config-and-subagents.md` Section 5, such as `ask_question` with `is_multi_select: true` in Antigravity or `AskUserQuestion` with `multiSelect: true` in Claude Code).
   - If all guides fit in one multi-select prompt for the active assistant, show a single checklist with labels in the form `<slug> (Ecosystem): <short summary>` or `<slug> (Language): <short summary>`.
   - If the assistant caps options per question (such as 4 options per question in Claude Code) or the catalog grows large, split into two multi-select questions (**Ecosystem guides** and **Language guides**, each with a `None` option) or present a numbered list in chat so the user can reply with numbers such as `1, 4`.
   - Note companion pairings from the **Companion guides** column above in one line, while allowing any combination.
   - If the user selects zero guides (or only `None`), confirm whether to save `default_contexts: none` or `default_contexts: auto`.
4. **Save `default_contexts` without modifying `skills/`.**
   - **Updating user-global config:** Edit `default_contexts:` in `~/.agents/develop-config.md`. If `~/.claude/rules/develop-config.md` exists as a static copy (not a symlink), update that copy too.
   - **Creating or updating a project-local override (`.agents/develop-config.md`):** Write **only** the `default_contexts:` overlay (not personal `repo_path`, `harness`, or model keys) so global updates continue to apply via key-level merging and the file stays safe to share or `.gitignore`. If the file already holds a full config, update only its `default_contexts:` line.
   - **No user-global config yet (outside installation):** Tell the user to install via `AGENTS.md` in the `uw-loci/agent-skills` repository, or create `~/.agents/develop-config.md` using the schema in `../develop/references/config-and-subagents.md`.
   - Report the updated config path and `default_contexts` value. Mention `/create-context-guide` if the user needs a guide for a stack not listed.

## Adding or updating a guide

Use [`/create-context-guide`](../create-context-guide/SKILL.md) to add a new team ecosystem or language guide and register it in the tables above.
