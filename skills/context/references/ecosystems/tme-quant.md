# TME-Quant Development Context

Context guide for the **TME-Quant / CurveAlign** tumor microenvironment and collagen fiber quantification stack under the `uw-loci` GitHub organization.

*Load alongside:* `../languages/python.md` (for `tme-quant` and `napari-curvealign`) and `../languages/java.md` + `fiji-imagej.md` (for `fiji-curvealign`).

## Scope and triggers

Use this guide when working in or referencing `uw-loci/tme-quant`, `uw-loci/fiji-curvealign`, `uw-loci/napari-curvealign`, `uw-loci/curvelets`, CurveAlign, CT-FIRE, `pycurvelets`, or `curvelops`.

## Architecture and repo boundaries

```text
uw-loci/curvelets (MATLAB)            <-- Historical reference implementation (CurveAlign & CT-FIRE)
         │  (translation & redesign, parity reference)
         ▼
uw-loci/tme-quant (Python, active)    <-- Core Python algorithms & unified cell/collagen engine
    ├──▶ uw-loci/fiji-curvealign      <-- Fiji (Java) plugin connector [CURRENT PRIORITY]
    └──▶ uw-loci/napari-curvealign    <-- Standalone napari plugin connector [ON HOLD]
```

## Where to look for X

| Repository | Role and status | When to touch it |
|---|---|---|
| [uw-loci/tme-quant](https://github.com/uw-loci/tme-quant) | **Active core Python repo.** Redesign and Python translation of CurveAlign unifying cell and collagen analysis (`src/pycurvelets` is the active core; `src/napari_curvealign` is legacy napari glue retained during transition). | Core algorithm work, data models, Python API, MATLAB parity tests, and core packaging (`uv`, `ruff`, `pytest`). Put new core algorithms in `src/pycurvelets`, not `src/napari_curvealign`. |
| [uw-loci/fiji-curvealign](https://github.com/uw-loci/fiji-curvealign) | **Fiji plugin connector (current priority).** Java/Maven Fiji plugin integrating `tme-quant` workflows for Fiji users. | Fiji UI commands, parameter wiring, ImageJ/Fiji data conversion, and Java-to-Python invocation (keep core math in `tme-quant`, not here). |
| [uw-loci/napari-curvealign](https://github.com/uw-loci/napari-curvealign) | **Standalone napari plugin connector (currently on hold).** Intended to hold only napari UI and plugin glue. | Do not add new features or refactor here unless explicitly requested; keep core logic in `tme-quant`. |
| [uw-loci/curvelets](https://github.com/uw-loci/curvelets) | **Original MATLAB codebase** (CurveAlign and CT-FIRE). | Read-only ground truth when verifying algorithmic intent, parameter defaults, or generating MATLAB parity baselines. |

## Sharp edges and testing invariants

- **Keep connectors thin.** Core quantitative algorithms and domain logic belong in `uw-loci/tme-quant`. `fiji-curvealign` (and later `napari-curvealign`) should act strictly as thin platform and UI connectors.
- **CurveLab optional backend (`curvelops`):** Full curvelet transforms depend on separately licensed external binaries (**CurveLab FDCT/FDCT3D** and **FFTW 2.x**) that cannot be redistributed on PyPI. In `tme-quant`, `curvelops` is an optional extra (`uv sync --extra curvelops`), and CI splits into a basic lane (`test-basic`) and a CurveLab lane (`test-curvelab`).
- **Test environment flags in `tme-quant`:**
  - Standard suite: `uv run pytest`
  - Curvelet tests: `TMEQ_RUN_CURVELETS=1` and `QT_QPA_PLATFORM=offscreen`
  - Strict MATLAB reference parity assertions: `TMEQ_VALIDATE_MATLAB=1`
- **Headless Qt / napari rule:** Never instantiate a live `napari.Viewer()` in automated tests (causes headless Qt crashes); rely on import-only smoke tests unless an explicit offscreen driver is configured.
- **Filesystem hygiene:** Tests must never write output files to the repository root; use `tmp_path` or `tempfile.TemporaryDirectory` and store deterministic test fixtures under `tests/test_resources/`.
- **MATLAB parity pitfalls:** Always double-check 1-based versus 0-based indexing, column-major (Fortran) versus row-major (C) flattening, and image axis order `(Y, X)` or `(Z, Y, X)` when porting routines from `uw-loci/curvelets`.

## Upstream policy and contribution boundaries

All four repositories are UW-LOCI owned. Respect CurveLab's separate academic and commercial licensing restrictions: never vendor or commit unredistributable CurveLab source or binaries into git or CI artifacts.
