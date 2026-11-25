# Reproducible, Immutable Artifacts

Apply when designing algorithms, pipelines, public APIs, releases, or data outputs for open-source scientific software.

- **Immutability & provenance.** Never mutate published releases or rewrite shared git history (`main` is permanent; do not force-push). Pin reproducible dependency graphs (`pom-scijava`, `uv.lock`, `pixi.toml`), record parameters, software versions, and random seeds needed to reproduce results, and keep computation deterministic where expected.
- **FAIR by default.** Keep artifacts Findable, Accessible, Interoperable, and Reusable: favor open standard formats, clear metadata, permissive open-source hygiene, and public documentation.
- **Separation of concerns.** Keep core scientific algorithms decoupled from GUI widgets and display state so the same logic runs cleanly inside interactive applications (Fiji, napari, QuPath) as well as scripts, batch pipelines, and automated tests.
- **SemVer & snapshot/dev version discipline.** Preserve backward compatibility for mature (`>= 1.0`) public APIs and published user workflows (macros, scripts, file formats); deprecate with migration guidance instead of breaking downstream scientists. Only delete legacy APIs in one wave for internal or `0.x` incubating code.
- **Advance snapshot/dev versions immediately when API scope grows.** Check `<version>` (`X.Y.Z-SNAPSHOT` in Maven) or `version` (`X.Y.Z.dev0` in Python) as soon as a change alters the public contract:
  - **New public API** on a non-zero patch (`Z > 0`, e.g., `2.4.1-SNAPSHOT` or `1.2.3.dev0`) → bump `MINOR` and reset `PATCH` to `0` (`2.5.0-SNAPSHOT` / `1.3.0.dev0`).
  - **Approved breaking change** on `>= 1.0` when `Y > 0` or `Z > 0` → bump `MAJOR` and reset to `(X+1).0.0-SNAPSHOT` / `.dev0`.
  - **Bug fixes or internal-only changes** → keep the current patch version.
