---
name: why
description: "Explain why code is designed a certain way using git history, commit messages, and PR discussions. Pass a symbol, file, or design decision after /why (use /how for runtime behavior)."
disable-model-invocation: true
---

# Why

If the user invokes `/why` without naming a symbol, file, behavior, or decision, ask what they want the history or rationale for before searching. If the user asks how code runs today or wants a guided walkthrough rather than design history, point them to `/how` or `/teach`.

Answer from the record, not guesses from current code alone. Read the commits, PR discussions, issues, and architecture decision records (ADRs) that introduced the target and each later change, and check linked sources if the trail is thin. Cite what the authors wrote, mark your own inferences as inferences, and state plainly what the record does not answer.
