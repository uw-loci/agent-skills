# Boundary Discipline

Apply when wiring validation, error handling, GUI dialogs, CLI parsing, config loading, or cross-language and framework adapters.

Validate, narrow types, and handle malformed input where data crosses a system boundary (CLI args, GUI inputs, config files, network payloads, file I/O, external APIs). Inside the boundary, trust internal types and avoid redundant re-validation or defensive nil checks.

- Parse raw external data into clean domain types at the boundary.
- Fail loudly rather than silently coercing data or falling back to a degraded backend. Never swallow precision loss, `dtype` or axis conversions, or missing optional dependencies without explicit user opt-in.
- Keep transport, GUI (Swing, JavaFX, napari), and cross-language IPC (Appose, PyImageJ/ScyJava) types out of core algorithms and business logic.
- Keep scientific computation and core logic in UI-agnostic, pure or well-isolated components so interactive GUIs, scripts, batch runners, and tests all call the same core through thin outer adapters.

Two checks: Is this data crossing a system boundary right now? If not, the guard is probably redundant. Does this algorithm depend on a GUI or IPC framework? If yes, separate the core computation from the thin adapter.
