---
name: in-your-own-words
description: "Have the agent restate your goal and problem in plain language and pause for confirmation before editing code. Use for /in-your-own-words."
disable-model-invocation: true
---

# In your own words

If no task or problem has been stated yet in the conversation, ask the user what they are working on first.

Otherwise, restate in your own words:

- What you think the user's goal is
- What problem they are trying to solve
- Any key constraints or assumptions you noticed

**Stop and wait for the user to confirm or correct your restatement before editing files or running code-changing commands** (unless called as an internal framing step by a read-only review skill such as `/interrogate` where the intent is already clear).
