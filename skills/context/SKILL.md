---
name: context
description: "Loads UW-LOCI multi-repo development context guides (Fiji/ImageJ/SciJava, TME-Quant/CurveAlign, QuPath extensions) and team Java/Python conventions on demand. Use automatically when working in a matching repository or language, or explicitly via /context <name>."
---

# Development Context Guides

Load **only** the guide(s) matching the active repository, org, or language so unrelated ecosystem maps stay out of the context window.

Check `default_contexts` in `develop-config.md` (`.agents/develop-config.md`, `~/.claude/rules/develop-config.md`, or `~/.agents/develop-config.md`):
- `auto` (default): match the active repo/language using the tables below.
- Comma-separated slugs (e.g., `tme-quant, python`): load those exact guides automatically.
- `none`: load guides only when the user explicitly requests `/context <name>`.

## Ecosystem guides

| Slug | Guide | Triggers (orgs, repos, topics) | Companion guides |
|---|---|---|---|
| `fiji-imagej` | [`references/ecosystems/fiji-imagej.md`](references/ecosystems/fiji-imagej.md) | `scijava/*`, `imglib/*`, `scifio/*`, `imagej/*`, `fiji/*`, `apposed/*`, `pom-scijava`, Fiji update sites, ImageJ2, ImgLib2, SCIFIO, PyImageJ, ScyJava, Appose, Jaunch, jgo, SciJava Ops, `scikit-ops` | `java` (plus `python` for PyImageJ/ScyJava/Appose/scikit-ops) |
| `tme-quant` | [`references/ecosystems/tme-quant.md`](references/ecosystems/tme-quant.md) | `uw-loci/tme-quant`, `uw-loci/fiji-curvealign`, `uw-loci/napari-curvealign`, `uw-loci/curvelets`, CurveAlign, CT-FIRE, `pycurvelets`, `curvelops` | `python` (plus `java` and `fiji-imagej` for `fiji-curvealign`) |
| `qupath` | [`references/ecosystems/qupath.md`](references/ecosystems/qupath.md) | `uw-loci/qupath-*`, `qupath/qupath`, QP-CAT, QuIET, QuPath extensions | `python` (when Appose Python workers are involved) |

## Language guides

| Slug | Guide | Triggers |
|---|---|---|
| `java` | [`references/languages/java.md`](references/languages/java.md) | Java / Maven repos across UW-LOCI, SciJava, ImageJ, Fiji, ImgLib2, SCIFIO (`pom.xml`, `.java`) |
| `python` | [`references/languages/python.md`](references/languages/python.md) | Python / `uv` repos across UW-LOCI (`pyproject.toml`, `.py`, `pytest`, `ruff`, `napari`, `pyimagej`, `appose-python`) |

## Adding or updating a guide

Use [`/create-context-guide`](../create-context-guide/SKILL.md) to add a new team ecosystem or language guide and register it in the tables above.
