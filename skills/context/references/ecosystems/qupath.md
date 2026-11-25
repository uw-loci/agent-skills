# QuPath Extensions Development Context

> **Starter draft — awaiting review by UW-LOCI QuPath lead.** Verify exact target QuPath version, extension repo list, and local testing commands with the extension maintainer (or run `/create-context-guide` to update).

Context guide for UW-LOCI extensions targeting the **QuPath** digital pathology platform.

*Load alongside:* `../languages/python.md` when working on Appose-backed Python components inside a QuPath extension.

## Scope & triggers

Use this guide when working in `uw-loci/qupath-*` repositories, QuPath extensions, QP-CAT, QuIET, or referencing `qupath/qupath`.

## Upstream policy & contribution boundaries (CRITICAL)

- **Do NOT use AI to author contributions to upstream `qupath/qupath`.** QuPath's lead maintainers maintain a strict anti-AI stance (see upstream [AI_POLICY.md](https://github.com/qupath/qupath/blob/main/AI_POLICY.md)) and are conservative about extension hooks in core QuPath.
- **Treat `qupath/qupath` strictly as read-only reference.** Never draft, open, or suggest submitting AI-generated PRs, patches, issue reports, or forum replies to upstream QuPath repositories.
- **Keep AI-assisted work strictly inside UW-LOCI-owned extension repos.** Design extensions to be self-contained against QuPath's public APIs without assuming upstream will merge helper hooks or accept extension-specific core changes.

## Build system exception: Gradle, not Maven

- Unlike SciJava/Fiji Java projects (which use Maven), **QuPath and QuPath extensions use Gradle** (Kotlin DSL `build.gradle.kts` / `settings.gradle.kts`) via QuPath's official convention plugin (`qupath-gradle-plugin` / `qupath-conventions`) and typically package distributable JARs with `shadowJar`.
- Do not attempt to migrate QuPath extensions to Maven, and keep dependencies aligned with the target QuPath version catalog declared in `settings.gradle.kts`.

## Where to look for X

| Repository | Role | Notes |
|---|---|---|
| [uw-loci/qupath-extension-fiber-analysis](https://github.com/uw-loci/qupath-extension-fiber-analysis) | Collagen fiber morphometrics (straightness, TWOMBLI-derived metrics, GLCM texture) in QuPath | Java QuPath extension bridged to embedded Python via **Appose**. |
| [uw-loci/qupath-extension-cell-analysis-tools](https://github.com/uw-loci/qupath-extension-cell-analysis-tools) | QP-CAT: multiplexed cell phenotyping, clustering, and spatial statistics in QuPath | Java QuPath extension + embedded scientific Python environment. |
| [uw-loci/qupath-catalog-mikenelson](https://github.com/uw-loci/qupath-catalog-mikenelson) | UW-LOCI QuPath extension catalog (including QuIET export toolkit and prototypes) | Reference for catalog metadata and extension distribution. |
| [qupath/qupath](https://github.com/qupath/qupath) | Upstream QuPath core application (GPLv3) | **Read-only reference** for inspecting public APIs and version changes. |
| [apposed/appose-java](https://github.com/apposed/appose-java) / [apposed/appose-python](https://github.com/apposed/appose-python) | Interprocess Java ↔ Python runtime bridge | Used by UW-LOCI QuPath extensions to invoke Python workflows cleanly. |

## Extension architecture guardrails

- **Isolate QuPath API calls behind thin adapters.** QuPath internals can shift between minor releases; wrap QuPath UI/model calls cleanly so core logic (and Python/Appose workers) stays testable and resilient to upstream API drift.
- **Avoid bundling duplicate platform JARs.** Rely on `qupath-conventions` so JavaFX / JavaCPP / QuPath core dependencies are provided at runtime rather than shadowed redundantly into the extension JAR.
- **Verify against a real QuPath build.** Unit tests cover pure logic, but verify extension discovery, menu registration, and Appose worker execution against the target QuPath release before shipping.

## Open items for maintainer review

- [ ] Confirm complete list of active `uw-loci` QuPath extension repos and catalog conventions.
- [ ] Confirm current target QuPath version(s) and JDK version pinned by `qupath-conventions`.
- [ ] Document local Gradle test/run commands and any Appose environment setup quirks.
