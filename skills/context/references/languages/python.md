# Python Conventions (UW-LOCI)

Targeted guardrails for Python repositories across UW-LOCI (`tme-quant`, `pyimagej`, `scyjava`, `appose-python`, and Python-backed QuPath/Fiji connectors). Defer standard Python syntax and formatting to `pyproject.toml` and `ruff`; focus here on UW-LOCI tooling and scientific pitfalls.

## Tooling & environment workflow

- **`uv` is the target project manager** (`pyproject.toml` + `uv.lock`). Prefer `uv sync` and `uv run <cmd>` (e.g., `uv run pytest`, `uv run ruff check .`) over manual `pip install` or ad-hoc virtualenv activation.
- **Lint & test defaults:** Use **Ruff** for linting/formatting and **pytest** for testing, honoring each repo's `pyproject.toml` configuration.
- **Native / JVM dependencies caveat:** `uv` manages Python packages cleanly, but repos that bridge Java or native libraries (`pyimagej`, `scyjava`, `appose`, CurveLab/FFTW) may also require **OpenJDK, Maven, conda-forge**, or separately built native binaries. Check the repo's README/CI workflows before assuming `uv sync` alone provisions the full runtime.
- **Layout:** Prefer `src/` package layout with explicit optional extras in `pyproject.toml` for heavy, GUI, or non-redistributable dependencies (for example, `uv sync --extra curvelops` in `tme-quant`).

## Scientific array & MATLAB-porting pitfalls

- **Verify axis ordering explicitly.** Document and assert array axis order at module boundaries (`(Z, Y, X)`, `(Y, X, C)`, `(X, Y, Z)`). Silent axis swaps between MATLAB, NumPy/napari, and ImageJ/ImgLib2 are a primary source of subtle scientific bugs.
- **Preserve `dtype` and numeric precision.** Avoid silent casts between `uint8`, `uint16`, `float32`, and `float64` across pipeline stages.
- **MATLAB-to-Python translation checks:**
  - Watch 1-based inclusive indexing vs. Python 0-based half-open slicing.
  - Watch Fortran (column-major) vs. C (row-major) reshape/ravel order (`order="F"` when matching MATLAB linear indexing).
  - Watch silent NumPy broadcasting differences vs. MATLAB matrix operations.
  - Pin numerical behavior against deterministic reference fixtures (e.g., MATLAB reference outputs) with explicit tolerances instead of eyeballing plots.

## Boundaries, GUIs & headless testing

- **Separate core algorithms from UI and IPC adapters.** Keep numerical/domain modules pure Python + NumPy/SciPy so they run fast in headless tests without requiring Qt, `napari`, or a running JVM.
- **Headless GUI discipline:** In Qt/`napari`-adjacent test suites, set `QT_QPA_PLATFORM=offscreen` and avoid instantiating a live `napari.Viewer()` in automated CI unless the repo specifically configures an offscreen viewer harness (import-only smoke tests prevent headless segfaults).
- **Clean test filesystem hygiene:** Never write test artifacts into the repository root; use pytest's `tmp_path` or `tempfile.TemporaryDirectory`, and store deterministic fixtures in the repo's designated test-resources directory.
- **Java interop:** Check whether the repo uses **Appose** (isolated process + shared memory) or **PyImageJ / ScyJava** (JPype in-process JVM). In PyImageJ test suites, check `conftest.py` for custom pytest flags (`--ij`, `--headless`, `--java`) and session-scoped gateway fixtures.
