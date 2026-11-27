---
name: no-comments
description: "Audit comments and suppressions before review using Comment Auditor, fix accepted findings, and offer structural encodings for claimed constraints. Use for /no-comments."
disable-model-invocation: true
---

# No comments

Run **Comment Auditor** on the scoped diff or files, review its report critically, and apply only accepted deletions and root-cause fixes.

Defer to Comment Auditor's fresh perspective, but verify every proposed change yourself.

## Scope

Use the caller's named files or diff. Otherwise use the current git diff against the base branch (default `main`), including the working tree.

## Steps

1. **Run Comment Auditor.** Read `develop-config.md` (`.agents/develop-config.md`, `~/.claude/rules/develop-config.md`, or `~/.agents/develop-config.md`) for `medium_effort_model` (default `inherit`; legacy fallback `review_model`) and `delegation_policy`.
   - When spawning a subagent, omit the model override for `inherit` (or legacy `inherit-parent` / `auto`). Use the registered `comment-auditor` agent if your coding assistant supports it; otherwise spawn a read-only general subagent whose prompt is [`references/comment-auditor.md`](references/comment-auditor.md) verbatim, followed by the scope.
   - **Deprecated or unsupported model fallback:** If your coding assistant rejects the configured model value, never retry the rejected value. Fall back immediately to `inherit` to finish the audit, and include a one-time deprecation notice in Step 6 naming the active `develop-config.md` path, the config key, the rejected value, the valid model values accepted by your assistant, and an offer to update `develop-config.md` and re-run Suite 3 Check 5 of `docs/validation.md`. Do not edit `develop-config.md` without user confirmation.
   - If your coding assistant has no subagent tool or `delegation_policy` is `single-agent`, follow [`references/comment-auditor.md`](references/comment-auditor.md) yourself in a dedicated fresh pass over the scope.
2. **Audit the report.** Reject any application-code edits, out-of-scope suggestions, deletions of protected keep-list exceptions, inaccurate `MUST KILL` claims, or flags against intentional, clear code.
   - Keep `MUST KILL` refactor flags for surprises in our own code; do not keep explanatory comments that paper over confusing local code.
   - Audit missed lint or type suppressions (`eslint-disable`, `@ts-ignore`, `@ts-expect-error`, `# noqa`, `# type: ignore`, `@SuppressWarnings`, etc.). Suppressions hiding correctness or safety bugs stay actionable `MUST KILL` items.
   - Before accepting or rejecting thin `IMPORTANT` or `do not remove` claims, trace the named symbol or run **why** on its git history.
   - Keep `REVIEW` items about unverified external rules intact and report them open to the user.
3. **Apply accepted comment deletions and trivial cleanups.** Delete accepted filler/narration comments. Fix trivial accepted `MUST KILL` items directly (deleting dead paths, dropping unused parameters, using the real API). If any accepted `MUST KILL` requires redesigning types or boundaries, run **architect** once for the accepted set before implementing.
4. **Implement scoped root-cause fixes.** Apply the smallest root-cause fix inside scope per `../develop/references/principles/fix-root-causes.md` and `../develop/references/principles/redesign-from-first-principles.md`. If the true root cause lies out of scope, land the smallest clean in-scope improvement and report the remainder open. Never add defensive symptom guards.
5. **Handle constraint comments.** For comments saying `do not remove`, `do not change wording`, or `talk to X before changing` (outside protected external exceptions), propose the cheapest in-scope structural check (type, runtime assertion, test, or lint rule). Ask the user before adding a new check; if approved, encode it and delete the comment. Otherwise delete redundant prose or keep only an explicit open note in your report.
6. **Report.** Summarize comments deleted, protected exceptions kept, open `REVIEW` items, accepted `MUST KILL` fixes applied, structural encoding offers, any out-of-scope follow-ups, and any model fallback notice if triggered.
