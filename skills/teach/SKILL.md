---
name: teach
description: "Explain a subsystem or code change in plain language at your pace, building up step by step with diagrams. Pass a topic, file, or diff after /teach."
disable-model-invocation: true
---

# Teach

**Explain what a thing is, how it works, and why it is built that way, in one plain account at the reader's pace. The goal is understanding, not code edits.**

If the user invokes `/teach` without naming a topic, subsystem, file, or change, ask what they want explained and what they are trying to do with it (onboarding, debugging, reviewing, or modifying it).

Teach sits on top of `how` and `why`. Orient yourself in the code, then run `how` for runtime behavior and `why` for design history and tradeoffs. Blend what they find into one plain explanation, lead with what matters to the reader, and go deeper when they ask. Reword freely for teaching, but keep `why`'s confidence labels intact (its hedges are factual findings, not style).

## Approach

1. **Choose the core takeaways.** Pick the few things the reader should walk away understanding based on why they are asking (changing it, reviewing it, debugging it, or learning it) and what they already know from the conversation. Skip what they plainly already know and focus depth where their question sits.
2. **Delegate discovery to `how` and `why`.** Read enough code to orient yourself, then run `how` and `why` and combine their findings. Respect `delegation_policy` per [`../develop/references/config-and-subagents.md`](../develop/references/config-and-subagents.md): run `how` via its read-only subagent alongside `why` when subagents are enabled, or run them sequentially in the main session under `single-agent`. Match depth to the question (both for a subsystem; one may suffice for a small change).
3. **Start with a plain definition, then build up.**
   - Name the thing and say what it is in everyday engineering terms, then tie it to this codebase ("in X, we use this to ...").
   - Walk through what happens when a user or caller runs the workflow (for example, loads a dataset, triggers a transform, or calls an API) when concrete flow makes the idea click. Listing functions and constants is reference, not teaching.
   - Give the smallest complete answer first (a few clear sentences, never a wall of text), then stop and let the reader steer deeper.
   - Never print framing labels such as "the one idea to hold onto", "the key insight", "at its core", or "TL;DR".
4. **Keep it conversational, not theatrical.**
   - Offer clear follow-up threads and follow the reader's lead.
   - No quizzes and no pacing theater. Do not print "Pause", ask them to repeat back, or announce "here is the tricky part". Just explain it clearly, then stop so they can respond.
   - If running one-shot with no interactive follow-up, deliver a complete concise explanation and list deeper threads at the end.
5. **Show, and build diagrams incrementally.**
   - Open the diff, code, or debugger output when showing the real artifact lands faster than prose.
   - For anything with three or more moving parts, draw a short series of diagrams where each redraws the last and adds one piece, rather than dumping one giant all-at-once diagram at the end.
   - Use Mermaid for flows and relationships where labels carry the meaning. For spatial ideas (geometry, layout, overlap, before-and-after state), use an image-generation tool if available (marker-on-whiteboard style with short labels) or a clean ASCII or Mermaid sketch. A single simple point needs no figure.

## Style

Run every explanation through **unslop**, written in plain spoken English the way you would explain it to a colleague:

- State the concrete mechanism rather than metaphors or previews. Target density: "Cache eviction runs in two steps, one for the lookup entry and one for the backing array. When memory exceeds the limit, both the entry and its pixel buffer are released."
- Use normal sentence case, no em dashes, and short sentences (one or two commas at most).
- Give each concept one name and keep it. Avoid mirror slogans ("A without B, or B without A") and tidy closers ("the rest follows").
- Treat these steps as instructions to you, not headings or labels to print.

**Reply:** the explanation itself, never a report about what steps you ran. Lead with the main point, then the plain account of what it is, how it works, and why, plus optional follow-up threads for `/how` or `/why`.
