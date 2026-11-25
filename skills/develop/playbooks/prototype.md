### Prototype

**You own the design decision, not production code. The prototype is a throwaway instrument. The real build follows Feature.**

This is the one playbook where strict polish and production abstractions invert. Optimize for learning speed so you pick the right design cheaply before committing production code.

1. **Scope the decision.** Name the exact design or empirical question the prototype settles (layout, interaction, API ergonomics, timing, or library behavior). If there is no open question, skip prototyping and route to **Feature**.
2. **Build throwaway in isolation.** Work in an isolated scratch directory or throwaway branch, completely separate from production source. Use the lightest stack that exercises the question (minimal HTML/CSS/JS, a small standalone script, or a minimal harness). No production abstractions or test suites.
3. **Compare concrete variants.** When choosing between 2–3 competing directions, make them easy to compare side by side (a simple switcher or side-by-side script output).
4. **Observe on the real surface.** For visual choices, render and inspect screenshots or live output. For behavioral or performance choices, run and print the real timings or outputs. The observation is the deliverable.
5. **Recommend and hand off.** Present variants explored, observed evidence, tradeoffs, and a concrete recommendation. State plainly that the prototype is throwaway. Hand the chosen direction to **Feature** (or **architect**) for the real implementation.

**Reply:** variants explored, observed evidence, tradeoffs, recommendation, and the scratch path.
