# Redesign from First Principles

Apply when integrating a new requirement into an existing design.

Do not bolt new requirements onto an existing design with patches and special cases. Redesign cleanly as if the requirement had been a foundational assumption from day one — while respecting SemVer compatibility boundaries for mature (`>= 1.0`) public APIs.

- Read all affected files and understand the current design.
- Ask: "If we were writing this from scratch with this requirement, what would we build?"
- Distinguish **internal or `0.x` incubating code** (reshape cleanly and delete obsolete paths in one wave) from **mature (`>= 1.0`) public library APIs** (design the clean new API first, then preserve existing public entry points via `@Deprecated` adapters with clear migration pointers rather than silently breaking downstream users).
- Propagate the change consistently through types, docs, examples, and callers, delivering in small, verifiable steps.
