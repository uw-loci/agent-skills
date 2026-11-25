# Sequence Verifiable Units

Apply to multi-step work (migrations, refactors, sweeps) and to how you structure commits and PRs.

Order work into small units that each end in a verifiable, green state. Never advance to the next unit while the current check is red.

- Treat each unit as a bracket: known-good state, one focused change, run the check, proceed.
- Run the per-unit check even when edits are generated or automated.
- Order commits so the history proves itself to a reviewer: failing regression test before the fix, dead-code subtraction before structural reshape, baseline measurement before optimization.
