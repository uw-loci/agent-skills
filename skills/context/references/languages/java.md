# Java Conventions (UW-LOCI / SciJava)

Targeted guardrails for Java repositories across UW-LOCI, SciJava, ImageJ, Fiji, ImgLib2, and SCIFIO. Defer formatting and standard Java idioms to project linters and `scijava/scijava-coding-style`; focus here on ecosystem-specific traps.

## Build system & dependency management

- **Maven is the standard** across SciJava, ImageJ, Fiji, ImgLib2, SCIFIO, and `fiji-curvealign`. Do not introduce Gradle into Maven-based repos.
  - **Sole exception:** QuPath extensions use QuPath's official Gradle convention plugin (`qupath-gradle-plugin`). See `../ecosystems/qupath.md`.
- **Extend `pom-scijava` (`org.scijava:pom-scijava`)** and respect its Bill of Materials (BOM). Never hardcode dependency versions that `pom-scijava` already manages, and never inherit from the obsolete `fiji/pom-fiji`.
- **Check target Java version before writing code.** Read `<maven.compiler.release>` / `<maven.compiler.source>` (or `pom-scijava` parent version) first:
  - Repos targeting the stable `ImageJ` + `Java-8` + `Fiji` update sites must stay **Java 8 compatible** (no `var`, `record`, `List.of()`, text blocks, or switch expressions).
  - Repos targeting `Fiji-latest` use **Java 21+**. Verify the active branch's target JDK before introducing modern language features.

## Coding style & API discipline

- **Authoritative style sources:** [scijava/scijava-coding-style](https://github.com/scijava/scijava-coding-style) and the [SciJava Coding Style Guide](https://imagej.net/develop/coding-style).
- **Naming:** Follow SciJava interface/class naming (avoid `I` prefixes on interfaces and `Impl` suffixes on default implementations; prefer `Foo` + `DefaultFoo`).
- **Binary & semantic compatibility:** Libraries in `scijava`, `imglib`, `scifio`, and `imagej` sit beneath dozens of downstream Fiji plugins. Preserve public API compatibility and follow SemVer; avoid breaking signatures casually.
- **Keep releases & CI aligned:** Shared Maven release, SemVer-check, and GitHub CI setup scripts live in [scijava/scijava-scripts](https://github.com/scijava/scijava-scripts). Check there before writing custom release or CI boilerplate.

## SciJava IoC & scientific Java patterns

- **Respect the `Context` lifecycle.** In SciJava/ImageJ2 code, inject services and plugins via `@Plugin` and `@Parameter` rather than manually constructing services with `new` or holding static global state. Dispose temporary `Context` instances in tests.
- **Avoid allocations in pixel hot loops.** In ImgLib2 image processing code, reuse `Cursor` / `RandomAccess` and primitive/type buffers; avoid Java Streams and autoboxing inside per-pixel loops.
- **Cross-language boundaries:** Isolate Java-to-Python calls behind thin adapters using **Appose** (`apposed/appose-java`, separate worker process with shared memory) or **ScyJava/PyImageJ** (in-process JVM bridge). Keep core domain logic decoupled from IPC glue.

## Testing & verification

- Run `mvn test` (or `mvn -Dtest=ClassName test` for fast iteration) and verify against the real POM configuration.
- For multi-repo changes, install upstream snapshots locally (`mvn install -DskipTests` or with tests) and verify the downstream consumer builds and passes against the updated artifact rather than assuming compatibility.
