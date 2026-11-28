---
name: sharpen
description: "Rewrite an underspecified prompt so it asks for deeper, verifiable work before you run it. Pass your draft prompt after /sharpen; returns the improved prompt without executing it."
disable-model-invocation: true
---

# Sharpen

Help the user turn a rough or surface-level prompt into a deeper, more verifiable prompt without expanding its scope.

If the user invokes `/sharpen` without a draft prompt or task, ask them to paste the prompt or describe the task they want sharpened.

Before rewriting the prompt, answer four concise points:

1. **Expert standard:** What a seasoned practitioner in this area would check or do that the draft prompt does not ask for yet.
2. **Primary sources:** The rawest source material to start from instead of secondary summaries.
3. **Concrete methods and tools:** The specific methods, commands, or verification tools that fit this task.
4. **Independent proof:** What external check (beyond agent or human opinion) proves the result is right.

Then write the sharpened prompt incorporating those four points. Have the rewritten prompt instruct the agent to prototype any design choice an experiment can settle and recommend an option from observed results, while leaving product or preference calls for the user to decide.

**Stop after presenting the rewritten prompt. Do not execute the task or edit files unless the user asks you to run it.** To verify intent before editing, point the user to `/in-your-own-words`; to execute the rewritten prompt, suggest passing it to `/develop`.
