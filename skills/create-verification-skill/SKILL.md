---
name: create-verification-skill
description: "Create a project-local verify-<app> skill that launches and tests your app, CLI, desktop tool, or library end to end with real proof. Run /create-verification-skill inside the target repository."
disable-model-invocation: true
---

# Create a verification skill

Every serious project needs a scripted way to drive the real software and prove behavior: launch it, exercise a feature the way a user would, and capture evidence. This skill generates a project-local skill (`<skills>/verify-<app>/`) tailored to the active repository.

`<skills>` is your coding assistant's project skill folder: `.agents/skills/` (recommended default, discovered by VS Code / GitHub Copilot, Antigravity, and Cursor), `.github/skills/` (VS Code / GitHub Copilot), `.claude/skills/` (Claude Code), or `.cursor/skills/` (Cursor). If the repository already keeps skills in one of these folders, use that folder; otherwise confirm the target folder with the user if unclear.

Write the generated skill for the next agent, not for a human. It will be read cold, mid-task, by an agent that has never seen the repository.

## 1. Inspect the repository first, ask only for gaps

Answer these from the codebase and ask the user only what you cannot observe:

- **User interface:** What does a user actually touch? A web UI, a CLI or terminal UI (TUI), a desktop app (such as Fiji/Swing, QuPath/JavaFX, or napari/Qt), an HTTP API, a mobile app, or a software library? A repo can have several; pick the primary one and note the rest.
- **Run:** How does the project build or start locally? Prefer the repo's own documented dev command (package scripts, Maven/Gradle, `uv`, Makefile, README quickstart). Note ports, environment variables, seed data, and auth.
- **Drive:** How can an agent interact with it programmatically? Use existing test drivers first: Playwright or Cypress specs, expect scripts, pseudo-terminal (PTY) helpers, curl-able endpoints, headless/offscreen desktop entry points (such as Fiji macros, `QT_QPA_PLATFORM=offscreen`, or Gradle/Maven integration tasks), or public-API driver scripts for libraries. Only then pick a generic recipe: browser or Chrome DevTools Protocol (CDP) for web and Electron, tmux/PTY for CLI/TUI, plain HTTP for services, or a minimal public-API runner for libraries.
- **Observe:** What evidence can be captured? Screenshots, terminal transcripts, response bodies, output files, logs, exit codes, or database state.
- **Isolate:** Can two instances run side by side (separate ports, data directories, profiles)? If not, state that clearly in the generated skill. Refusing to double-drive a shared instance beats corrupting the user's session.

If the checkout fails to build or start as-is, report the exact failure and ask the user before patching product code; a skill written against a broken base teaches wrong steps. When an irrelevant missing asset blocks startup (such as a sample config or empty static directory), the generated skill may create it, clearly marked as temporary verification setup, and remove it during cleanup.

## 2. Generate the skill

Write `<skills>/verify-<app>/SKILL.md` with YAML frontmatter (`name: verify-<app>` and a `description` that names the app, its interface, and when to use it; without frontmatter the skill never registers) and these sections, grounded in what you actually observed (leave no placeholders):

- **Launch:** The exact command that starts or builds the project for verification, and how to tell it is ready (a log line, a prompt, or a successful build). Launch must reach a usable state from an empty data directory, including migrations and seed data. Ready means usable, not merely that a process listens on a port (a database health check can pass while init scripts are still running). Include teardown. For a short-lived CLI, TUI, or library, launch means building or installing dependencies once, then starting each run in its own isolated terminal session or temp directory.
- **Doctor:** One read-only check that answers "is this instance ready to drive?" (process up, right version or build, port owned by this run, valid auth, or required native/JVM dependencies present). An agent runs this first whenever anything looks off.
- **Drive:** Concrete commands or selectors from this repo, not generic examples. Prefer stable handles (ARIA accessibility labels, data attributes, prompt strings, CLI flags, route paths, or public API calls) over coordinates and tab order.
- **Evidence:** What to capture for proof and where it is saved. State the proof standards: exercise the real user path rather than internal setters or test-only endpoints; capture both the action and the resulting state; verify side effects (files written, rows inserted, messages sent) alongside visible output; mock only where a production boundary already isolates an external system. When using a dry-run or test mode, observe what it actually skips (files, network, git refs) rather than trusting its flag name.
- **Cleanup:** How to tear down instances the run created. Never kill by process name; kill only the processes you started. Cleanup removes temporary instances and scratch state, never the evidence. Proof artifacts must survive teardown in a location the skill names.
- **Helpers:** Any helper script the skill ships must be executable and its exact invocation must appear in the skill body.

## 3. Seed the feature map

Create `<skills>/verify-<app>/features/README.md` plus one file per major user-facing feature (aim for the top 3 to 5 features to start, derived from routes, commands, menus, public entry points, or docs). Follow the shape in [`references/feature-map-example/`](references/feature-map-example/), with a README index and one file per feature.

Each feature file answers from the user's point of view (POV): what the feature is, how to reach it, how to drive it with the verification tool, and what observable end state proves it works. Use the four H2 headings: `Sub-features`, `How to get to it (user POV)`, `Driving it with <tool>`, and `Gotchas`. If seed data lacks a precondition a journey needs, report a failure and record the reason in `Gotchas`. Never weaken the check to make it pass.

## 4. Prove the generated skill before handing it over

Run its own instructions end to end once: launch, doctor, drive one mapped feature (the map exists so later runs can cover the rest), capture evidence, and clean up. After cleanup, confirm the evidence still exists at the named location (a cleanup that deletes the proof fails this step). Fix what fails, and run cleanup after every failed iteration so broken attempts do not strand processes or ports.

A generated skill that was never executed is a draft, not a deliverable. If you proved it in a stand-in environment (such as a container instead of a fresh VM, or a local stack instead of a remote one), list every setup step the stand-in performed that the real target will not.

## 5. Offer the maintenance loop

Point the user at `/maintain-verification-skill` for keeping the verification skill and feature map accurate as the project evolves. Suggest a cadence only if they ask.
