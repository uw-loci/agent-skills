---
name: unslop
description: "Rewrite prose to remove common AI writing patterns, filler, and vague wording while keeping your meaning. Pass text or a file path after /unslop (or run bare to clean the previous draft)."
disable-model-invocation: true
---

# Unslop

Edit text to remove common AI writing patterns and filler. Scan for the patterns below, then rewrite. Preserve meaning and match the intended tone.

If the user passes text or a file path, rewrite that target. If invoked bare (`/unslop`) after a draft in this conversation, rewrite the previous draft. If there is no prior draft, ask what text or file to clean up. For structuring full documentation, READMEs, RFCs, or PR descriptions rather than prose-only cleanup, point the user to `/technical-writing`.

1. No trailing "-ing" phrases that add no fact ("highlighting...", "ensuring...").
2. No vague attributions ("experts believe"). Name the source or delete.
3. No AI vocabulary: additionally, crucial, delve, enhance, foster, landscape, pivotal, showcase, testament, underscore, vibrant.
4. Say "is" or "has", not "serves as", "stands as", "boasts", "features".
5. No "not just X, but Y". State the point directly.
6. Do not force ideas into threes.
7. One name per thing. Repeat it.
8. No "from X to Y" unless X and Y sit on a real scale.
9. No em dashes, en dashes, or hyphens used as dashes, and no parentheses in their place. Use a period or a comma.
10. A colon goes before a list or an example, never mid-sentence as a connector.
11. Do not bold every proper noun or acronym.
12. No bold label and colon that restates its line ("**Performance:** Performance improved..."). A bold lead-in that ends in a period and adds new detail is fine.
13. Sentence case headings.
14. No decorative emojis.
15. Straight quotes.
16. No chatbot phrases ("I hope this helps!", "Let me know if...").
17. No praise or agreement openers. Respond directly.
18. Cut filler. "In order to" becomes "to". Delete "it is important to note that".
19. One hedge at most: "may".
20. No generic conclusions. State specific plans or facts.
21. No vague metaphorical nouns where a concrete word fits: substrate, wedge, vector, nexus, primitive, harness, surface, scaffolding, paradigm, ratchet, north star, flywheel. Keep literal domain terms when they are the actual technical name (for example, a Java `primitive`, mathematical `vector`, test `harness`, or 3D `surface`).
22. Say what it does, not how it feels. Name the mechanism or the number. Cut a sentence that could appear unchanged in another project's docs.
23. One idea per sentence. Split a sentence the reader has to reread.
24. Active voice. Name the actor unless it is unknown or does not matter.
25. Cut adverbs or use a stronger verb. Give the number.
26. Use the plain word: "use", not "utilize" or "leverage".
27. No metaphor, aphorism, personified code, or figurative verb where a literal phrase exists.
28. Write whole sentences with their articles and verbs. Spell out arrows and abbreviations.
