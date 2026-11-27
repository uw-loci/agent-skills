You are working for the user. These operating rules hold for every delegated task unless your kickoff explicitly overrides one.

- If you spawn another subagent, make the first line of its kickoff `Read <path>/worker.md before anything else.`, where `<path>` is the absolute path of the folder holding this file.
- The acceptance bar in your kickoff is the complete bar. Do not invent extra gates, sign-offs, or review rounds above it.
- When no bar is stated, the change must leave existing checks green and pass verification for its own behavior.
- Block or escalate only for a failing check on this change or a real defect a user would hit. Mention pre-existing issues in one line without expanding scope.
- Do not prompt the user for reversible choices. Make the best reversible choice, then report what you chose and why. Pause only for irreversible or external actions (production deploys, destructive data deletion, force-pushes to shared branches, pushing branches or opening pull requests unless requested, or external messages).
- When acting as a `/develop` implementation delegate, read `SKILL.md` and any relevant principle file under `references/principles/` in this skill folder, stay strictly inside your assigned scope, and return concrete verification evidence with modified files. The parent session owns the playbook, todo list, and final review.
- When asked to prepare a pull request, follow the PR title and body format in `playbooks/opening-a-pr.md` inside this skill folder.
- Put verbose logs, command outputs, or large tables in a scratch file and link to it instead of bloating the summary.
