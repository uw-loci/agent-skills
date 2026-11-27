---
name: architect
description: "Compare two structural designs (types, signatures, and module boundaries) before writing code, then pause for approval. Pass the feature, bug, or boundary you want to design after /architect."
disable-model-invocation: true
---

# Architect

If the user invokes `/architect` without naming a feature, change, or boundary, ask what they want to design and what constraints apply before proceeding.

1. Trace every file, module, and caller the change touches.
2. Sketch two meaningfully different structural designs (types, signatures, and module boundaries).
3. Recommend the design where each piece of state has one owner, each task has one supported path, and callers need to know the least. Redesign cleanly rather than adding special-case patches when workarounds repeat.
4. Present both sketches, their tradeoffs, and your recommendation:
   - **Standalone `/architect` (or any breaking, public-API, or contested boundary change inside `/develop`):** Stop and wait for user approval before writing production code.
   - **Reversible internal boundary choice during an active `/develop` run:** Record the chosen shape and rationale concisely, then continue with the playbook.

For a large or contested design, offer the **arena** skill instead of sketching alone (check `delegation_policy` in `develop-config.md` per [`../develop/references/config-and-subagents.md`](../develop/references/config-and-subagents.md); under `single-agent`, ask before launching parallel candidates and note the token multiplier).
