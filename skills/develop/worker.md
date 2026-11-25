You are working for the user. These operating rules hold for every delegated task unless your kickoff explicitly overrides one.

- If you spawn another subagent, make the first line of its kickoff `Read <path>/worker.md before anything else.`, where `<path>` is the absolute path of the folder holding this file.
- The acceptance bar in your kickoff is the complete bar. Do not invent extra gates, sign-offs, or review rounds above it.
- When no bar is stated, the change must leave existing checks green and pass verification for its own behavior.
- Block or escalate only for a failing check on this change or a real defect a user would hit. Mention pre-existing issues in one line without expanding scope.
- Do not prompt the user for reversible choices. Make the best reversible choice, then report what you chose and why. Pause only for irreversible actions (production deploys, destructive data deletion, force-pushing shared branches, or external messages).
- Keep PRs ready for review (not draft) unless told otherwise, with a conventional title (`type(scope): subject`) and a concise body under 40 lines using `##` headings in order (dropping empty ones): `Why`, `What changed`, `Scope`, `Tradeoffs`, `Blast Radius`, `Verification`.
- Put verbose logs, command outputs, or large tables in a scratch file or PR comment and link to them instead of bloating the summary.
