# Fiji / ImageJ / SciJava Development Context

Context guide for the multi-org **Fiji / ImageJ / SciJava / ImgLib2 / SCIFIO / Appose** bioimage software stack, which converges into the Fiji desktop application and its Python bridges.

*Load alongside:* `../languages/java.md` (primary stack) and `../languages/python.md` (for `pyimagej`, `scyjava`, `appose-python`, or `scikit-ops`).

## Scope and triggers

Use this guide when working in or referencing repositories under `github.com/scijava`, `github.com/imglib`, `github.com/scifio`, `github.com/imagej`, `github.com/fiji`, or `github.com/apposed` (Fiji, ImageJ 1.x or ImageJ2, SciJava, ImgLib2, SCIFIO, PyImageJ, ScyJava, Appose, Jaunch, jgo, SciJava Ops, or `scikit-ops`).

## Architecture and layering

```text
Fiji Application (fiji/fiji)  +  Update Sites (Fiji stable [Java 8] vs. Fiji-latest [Java 21+])
  ├── Launchers & Updater:  apposed/jaunch (native) | scijava/app-launcher | imagej/imagej-updater
  ├── Desktop UI & Scripts: scijava-ui-swing | imagej-ui-swing | scijava/script-editor
  ├── ImageJ2 & IJ1 Bridge: imagej/imagej2 | imagej-common | imagej-legacy + ij1-patcher -> imagej/imagej (IJ 1.x)
  ├── Ops Ecosystem (3 generations, see below):
  │     imagej/imagej-ops (legacy) | scijava/scijava (SciJava Ops) | apposed/scikit-ops (+ fiji-skopkit)
  ├── Data & I/O Layers:    imglib/imglib2 (+ algorithm/roi/cache/unsafe) | scifio/scifio (+ bf-compat -> ome/bio-formats)
  ├── IoC & BOM Foundation: scijava/scijava-common | scijava/pom-scijava (BOM) | scijava/scijava-scripts
  └── Python / IPC Bridges: imagej/pyimagej + scijava/scyjava + apposed/jgo (in-process JVM)
                            apposed/appose (-java / -python) (interprocess shared-memory workers)
```

## Critical invariants

### 1. Update-site and Java version split (DO NOT MIX)

See [ImageJ List of Update Sites](https://imagej.net/list-of-update-sites/):

- **Stable (Java 8 End-of-Life release):** Built from the `ImageJ` + `Java-8` + `Fiji` update sites. Code targeting this channel must stay **Java 8 compatible**.
- **Active development (`Fiji-latest`):** Tracks **Java 21+**.
- **BOM synchronization:** `scijava/pom-scijava` is the authoritative Bill of Materials kept in sync with `Fiji-latest`. Never inherit from the obsolete `fiji/pom-fiji`. Temporary version-property pins in a component's `pom.xml` are acceptable when a newly released dependency is not yet managed by a released `pom-scijava`; always remove obsolete pins whenever updating the `pom-scijava` parent version.

### 2. The three Ops frameworks (common agent trap)

| Framework | Repository | Role and status |
|---|---|---|
| **ImageJ Ops** | [imagej/imagej-ops](https://github.com/imagej/imagej-ops) | Original Java ops framework; now **largely archived and maintenance-only**. |
| **SciJava Ops** | [scijava/scijava](https://github.com/scijava/scijava) | Redeveloped next-gen SciJava (future SciJava 2/3 direction) housing `scijava-ops` (graduated from archived `scijava/incubator`). |
| **scikit-ops** | [apposed/scikit-ops](https://github.com/apposed/scikit-ops) | Appose-powered layer (`skop` + `opspec` + isolated `pixi.toml` environments) unifying **algorithm and host environment** so one runtime can call algorithms with conflicting dependencies; connects to Fiji via `apposed/fiji-skopkit` and napari via `apposed/napari-skopkit`. |

## Where to look for X

| Need / Subsystem | Repository / Source | Notes |
|---|---|---|
| **BOM and Maven parent** | [scijava/pom-scijava](https://github.com/scijava/pom-scijava) | Single source of truth for dependency versions across the stack. |
| **Release and CI automation** | [scijava/scijava-scripts](https://github.com/scijava/scijava-scripts) | Shared scripts for Maven releases, SemVer checks, and GitHub CI setup; new shared infra scripts belong here. |
| **Coding style** | [scijava/scijava-coding-style](https://github.com/scijava/scijava-coding-style) and [Coding Style Wiki](https://imagej.net/develop/coding-style) | Formatter config and SciJava naming and API guidelines. |
| **Inversion of Control (IoC) container and plugins** | [scijava/scijava-common](https://github.com/scijava/scijava-common) | `@Plugin`, `@Parameter`, `Context`, `Service`, module execution. |
| **Expression parsing** | [scijava/parsington](https://github.com/scijava/parsington) | Infix-to-postfix mathematical expression parser. |
| **Core N-D arrays and math** | [imglib/imglib2](https://github.com/imglib/imglib2) | Plus `imglib2-algorithm`, `imglib2-roi`, `imglib2-cache`, `imglib2-unsafe` (> `Integer.MAX_VALUE` arrays). |
| **Image I/O** | [scifio/scifio](https://github.com/scifio/scifio) | Plus `scifio-bf-compat` (bridging to `ome/bio-formats`), `scifio-lifesci`, `scifio-labeling`. |
| **ImageJ 1.x and IJ2 core** | [imagej/imagej](https://github.com/imagej/imagej), [imagej/imagej2](https://github.com/imagej/imagej2), [imagej/imagej-common](https://github.com/imagej/imagej-common) | IJ 1.x upstream, IJ2 application layer, and IJ2 `Dataset` data model. |
| **IJ 1.x compatibility layer** | [imagej/imagej-legacy](https://github.com/imagej/imagej-legacy) and [imagej/ij1-patcher](https://github.com/imagej/ij1-patcher) | Bridges IJ 1.x and IJ2; bytecode-level IJ1 patching lives in `ij1-patcher`. |
| **Swing UI and Script Editor** | [scijava/scijava-ui-swing](https://github.com/scijava/scijava-ui-swing), [imagej/imagej-ui-swing](https://github.com/imagej/imagej-ui-swing), [scijava/script-editor](https://github.com/scijava/script-editor) | Desktop UI plus `scijava/scripting-*` language plugin implementations. |
| **Updater and Launchers** | [imagej/imagej-updater](https://github.com/imagej/imagej-updater), [scijava/app-launcher](https://github.com/scijava/app-launcher), [apposed/jaunch](https://github.com/apposed/jaunch) | Update sites (`imagej-updater`), Java bootstrap (`app-launcher`), and modern native launcher (`jaunch`). |
| **Fiji distribution** | [fiji/fiji](https://github.com/fiji/fiji) | Top-level Fiji assembly and distribution packaging. |
| **Python and IPC bridges** | [imagej/pyimagej](https://github.com/imagej/pyimagej), [scijava/scyjava](https://github.com/scijava/scyjava), [apposed/jgo](https://github.com/apposed/jgo), [apposed/appose](https://github.com/apposed/appose) | In-process JVM access (`pyimagej`, `scyjava`, `jgo`) compared with zero-copy interprocess workers (`appose-java` and `appose-python`). |
| **Documentation / Wiki** | [imagej/imagej.github.io](https://github.com/imagej/imagej.github.io) | Public ImageJ / Fiji / SciJava documentation site ([imagej.net/develop/](https://imagej.net/develop/)). |
| **Search, Javadoc, and LOCI Guides** | [search.imagej.net](https://search.imagej.net/), [javadoc.scijava.org](https://javadoc.scijava.org/), [uw-loci.github.io](https://uw-loci.github.io/) | Cross-repo code search, central live API Javadoc, and UW-LOCI philosophy and debugging articles. |
| **Community Channels** | [forum.image.sc](https://forum.image.sc/) and [imagesc.zulipchat.com](https://imagesc.zulipchat.com/) | Public user and community support forum and live or async developer chat. |

## Upstream policy and contribution boundaries

- All `scijava`, `imglib`, `scifio`, `imagej`, `fiji`, and `apposed` repos are community open-source projects (mostly BSD-2-Clause or permissive licenses, with IJ 1.x in the public domain and select GPL plugins in Fiji).
- Keep PRs tightly scoped to the repo that actually owns the responsibility in the table above; avoid cross-repo hacks or version pins that fight `pom-scijava`.
