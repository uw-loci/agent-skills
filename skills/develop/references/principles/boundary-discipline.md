# Boundary Discipline

Apply when wiring validation, error handling, CLI parsing, config loading, or framework adapters.

Validate, narrow types, and handle malformed input where data crosses a system boundary (CLI args, config files, network payloads, external APIs, user input). Inside the boundary, trust internal types: avoid redundant re-validation and defensive nil checks.

- Parse raw external data into domain types at the boundary.
- Keep transport and framework types out of core business logic.
- Keep core business logic in pure functions; keep the shell or adapter layer thin.

Two checks: Is this data crossing a system boundary right now? If not, the guard is probably redundant. Can this logic live in a pure function called by a thin adapter? If yes, extract it.
