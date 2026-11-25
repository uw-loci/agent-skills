# Model the Domain

Apply when writing stateful logic, growing conditionals, or code that repeats the same shape assumptions across files.

Encode the domain in a data structure instead of scattering it across conditionals. The right structure makes invalid states unrepresentable and deletes branches.

- Reach for a state machine instead of scattered booleans or phase flags.
- Use a typed model or discriminated union instead of loose parameters and repeated checks across files.
- Use a map, table, or registry instead of sprawling `if/else` or `switch` chains.
- Do not force abstractions. Keep boring code when the shape is clear, local, and unlikely to grow. Distrust any abstraction that adds indirection without deleting branches or invalid states.

Warning sign: a feature forces you to add one more branch to an `if/else` chain or a second boolean that must stay in sync with the first.
