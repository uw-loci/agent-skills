# Multi-phase plan

**You own the plan, not the code. The plan is a checklist an implementer can execute unit by unit and a reviewer can audit from evidence.** Do not implement production code during this playbook.

1. **Skip when small.** If the change is one or two files with an obvious approach, say so and route directly to [Feature](feature.md) or [Bug fix](bug-fix.md).
2. **Settle empirical forks first.** Resolve unknown behavior or design questions via [Prototype](prototype.md) before locking in the plan. Ask the user only about product or preference calls no experiment can settle.
3. **Write the plan.** Open with what changes, the ordered phases or PR IDs, and a dependency graph showing which units can run in parallel versus sequentially and which files each touches.
4. **Detail each verifiable unit.** Give each phase or PR concrete checkboxes for:
   - Prerequisites and dependencies
   - Files touched
   - The single change being delivered (read [Sequence Verifiable Units](../references/principles/sequence-verifiable-units.md))
   - Observable outcome
   - Verification criteria (unit checks plus live end-to-end verification on the real app, CLI, or API; performance checks when relevant, naming baseline and failure threshold)
   - Review gates (flag user-facing or high-risk phases that need human review before continuing)
5. **Hand back the plan and stop.** Wait for the user's approval before starting implementation.

**Reply:** plan location or summary, ordered phases with dependencies and review gates, principles applied, and any remaining unknowns.
