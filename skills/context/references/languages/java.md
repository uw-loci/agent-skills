# Java Conventions (UW-LOCI / SciJava)

Targeted guardrails for Java repositories across UW-LOCI, SciJava, ImageJ, Fiji, ImgLib2, and SCIFIO. Defer formatting and standard Java idioms to project linters and `scijava/scijava-coding-style`; focus here on ecosystem-specific traps.

## Build system and dependency management

- **Maven is the standard** across SciJava, ImageJ, Fiji, ImgLib2, SCIFIO, and `fiji-curvealign`. Do not introduce Gradle into Maven-based repos.
  - **Sole exception:** QuPath extensions use QuPath's official Gradle convention plugin (`qupath-gradle-plugin`). See `../ecosystems/qupath.md`.
- **Extend `pom-scijava` (`org.scijava:pom-scijava`)** and rely on its Bill of Materials (BOM) by default. Never inherit from the obsolete `fiji/pom-fiji`.
  - **Temporary version property overrides:** Pinning a component version property in `pom.xml` is acceptable temporarily when that component has a newer release that no `pom-scijava` release manages yet. Whenever you later bump the `pom-scijava` parent version, audit and remove any pinned version properties that the new BOM now covers.
- **Check target Java version before writing code.** Read `<maven.compiler.release>` or `<maven.compiler.source>` (or the `pom-scijava` parent version) first:
  - Repos targeting the stable `ImageJ` + `Java-8` + `Fiji` update sites must stay **Java 8 compatible** (no `var`, `record`, `List.of()`, text blocks, or switch expressions).
  - Repos targeting `Fiji-latest` use **Java 21+**. Verify the active branch's target JDK before introducing modern language features.

## Coding style and API discipline

- **Authoritative style and docs:** [scijava/scijava-coding-style](https://github.com/scijava/scijava-coding-style), [SciJava Coding Style Guide](https://imagej.net/develop/coding-style), [ImageJ Developer Docs](https://imagej.net/develop/), and [UW-LOCI Software Articles](https://uw-loci.github.io/) (including *Developing LOCI Software* and *Debugging Techniques*).
- **Cross-repo discovery:** Search across the stack at [search.imagej.net](https://search.imagej.net/) and inspect published API contracts at [javadoc.scijava.org](https://javadoc.scijava.org/).
- **Naming:** Follow SciJava interface and class naming (avoid `I` prefixes on interfaces and `Impl` suffixes on default implementations; prefer `Foo` and `DefaultFoo`).
- **Binary and semantic compatibility:** Libraries in `scijava`, `imglib`, `scifio`, and `imagej` sit beneath dozens of downstream Fiji plugins. Preserve public API compatibility and follow SemVer; immediately check `<version>` (`X.Y.Z-SNAPSHOT`) when adding public API on a non-`.0` patch and advance to `X.(Y+1).0-SNAPSHOT`.
- **Keep releases and CI aligned:** Shared Maven release, SemVer-check, and GitHub CI setup scripts live in [scijava/scijava-scripts](https://github.com/scijava/scijava-scripts). Check there before writing custom release or CI boilerplate.

## SciJava Inversion of Control (IoC) and scientific Java patterns

- **Respect the `Context` lifecycle.** In SciJava and ImageJ2 code, inject services and plugins via `@Plugin` and `@Parameter` rather than manually constructing services with `new` or holding static global state. Dispose temporary `Context` instances in tests.
- **Avoid allocations in pixel hot loops.** In ImgLib2 image processing code, reuse `Cursor` or `RandomAccess` and primitive or type buffers; avoid Java Streams and autoboxing inside per-pixel loops.
- **Cross-language boundaries:** Isolate Java-to-Python calls behind thin adapters using **Appose** (`apposed/appose-java`, separate worker process with shared memory) or **ScyJava/PyImageJ** (in-process JVM bridge). Keep core domain logic decoupled from IPC glue.

## Testing and verification

- Run `mvn test` (or `mvn -Dtest=ClassName test` for fast iteration) and verify against the real POM configuration.
- For multi-repo changes, install upstream snapshots locally (`mvn install -DskipTests` or with tests) and verify the downstream consumer builds and passes against the updated artifact rather than assuming compatibility.
