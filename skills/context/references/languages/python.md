# Python Conventions (UW-LOCI)

Targeted guardrails for Python repositories across UW-LOCI (`tme-quant`, `pyimagej`, `scyjava`, `appose-python`, and Python-backed QuPath and Fiji connectors). Defer standard Python syntax and formatting to `pyproject.toml` and `ruff`; focus here on UW-LOCI tooling and scientific pitfalls.

## Tooling and environment workflow

- **`uv` is the target project manager** (`pyproject.toml` and `uv.lock`). Prefer `uv sync` and `uv run <cmd>` (for example, `uv run pytest`, `uv run ruff check .`) over manual `pip install` or ad-hoc virtualenv activation.
- **Lint and test defaults:** Use **Ruff** for linting and formatting and **pytest** for testing, honoring each repo's `pyproject.toml` configuration.
- **Native and JVM dependencies caveat:** `uv` manages Python packages cleanly, but repos that bridge Java or native libraries (`pyimagej`, `scyjava`, `appose`, CurveLab/FFTW) may also require **OpenJDK, Maven, conda-forge**, or separately built native binaries. Check the repo's README and CI workflows before assuming `uv sync` alone provisions the full runtime.
- **Layout:** Prefer `src/` package layout with explicit optional extras in `pyproject.toml` for heavy, GUI, or non-redistributable dependencies (for example, `uv sync --extra curvelops` in `tme-quant`).
- **SemVer and dev versioning:** When adding new public API while `version` in `pyproject.toml` sits on a non-`.0` patch (for example, `1.2.3.dev0`), immediately advance `MINOR` and reset `PATCH` to `0` (`1.3.0.dev0`).

## Scientific array and MATLAB-porting pitfalls

- **Verify axis ordering explicitly.** Document and assert array axis order at module boundaries (`(Z, Y, X)`, `(Y, X, C)`, `(X, Y, Z)`). Silent axis swaps between MATLAB, NumPy/napari, and ImageJ/ImgLib2 are a primary source of subtle scientific bugs.
- **Preserve `dtype` and numeric precision.** Avoid silent casts between `uint8`, `uint16`, `float32`, and `float64` across pipeline stages.
- **MATLAB-to-Python translation checks:**
  - Watch 1-based inclusive indexing versus Python 0-based half-open slicing.
  - Watch Fortran (column-major) versus C (row-major) reshape and ravel order (`order="F"` when matching MATLAB linear indexing).
  - Watch silent NumPy broadcasting differences compared with MATLAB matrix operations.
  - Pin numerical behavior against deterministic reference fixtures (for example, MATLAB reference outputs) with explicit tolerances instead of eyeballing plots.

## Boundaries, GUIs, and headless testing

- **Separate core algorithms from UI and IPC adapters.** Keep numerical and domain modules pure Python + NumPy/SciPy so they run fast in headless tests without requiring Qt, `napari`, or a running JVM.
- **Headless GUI discipline:** In Qt or `napari`-adjacent test suites, set `QT_QPA_PLATFORM=offscreen` and avoid instantiating a live `napari.Viewer()` in automated CI unless the repo specifically configures an offscreen viewer driver (import-only smoke tests prevent headless segfaults).
- **Clean test filesystem hygiene:** Never write test artifacts into the repository root; use pytest's `tmp_path` or `tempfile.TemporaryDirectory`, and store deterministic fixtures in the repo's designated test-resources directory.
- **Java interop:** Check whether the repo uses **Appose** (isolated process with shared memory) or **PyImageJ / ScyJava** (JPype in-process JVM). In PyImageJ test suites, check `conftest.py` for custom pytest flags (`--ij`, `--headless`, `--java`) and session-scoped gateway fixtures.
