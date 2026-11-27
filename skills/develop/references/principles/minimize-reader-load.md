# Minimize Reader Load

Apply when reviewing, cleaning, or evolving code that is hard to trace, or before building on top of cluttered structure.

Reader load has two axes: how many layers a reader must trace between question and answer, and how much hidden or mutable state they must hold in their head. Guard both.

- **Subtract before you add.** Remove dead code, redundant validators, and unused references first, then build on the simpler base.
- **Collapse forwarding layers.** Inline one-caller wrappers, single-implementation adapters, and pass-through methods.
- **Shrink state scope.** Prefer return values over mutation, locals over fields, fields over module state, and derived values over manually synced copies.
- **Honor least surprise in function contracts.** Match behavior to the function name and signature, and keep parameter order, return conventions, and error signaling consistent across sibling functions. Avoid hidden side effects in read or query operations and unexpected in-place mutation of caller-owned inputs.
- **Name invariants once** at the boundary instead of repeating checks in every consumer.

The test: can a new reader answer "where does X come from?" and "what can change X?" in under 30 seconds? If not, cut layers or cut state.
