---
name: audit-comments
description: "Audit comments and lint or type suppressions for clutter or hidden workarounds, then ask before deleting or refactoring. Defaults to your current branch diff, or pass files or paths after /audit-comments."
disable-model-invocation: true
---

# Audit comments

Run **Comment Auditor** on the scoped diff or files, review its report critically, and apply only approved deletions and root-cause fixes.

Defer to Comment Auditor's fresh perspective, but verify every proposed change yourself.

## Scope

Use the files, paths, or diff the user names. Otherwise use the current git diff against the repository's default branch (for example, `main` or `master`), including the working tree. If there is no named scope and the diff is empty, ask the user which files or commits they want audited.

## Steps

1. **Run Comment Auditor.** Read [`../develop/references/config-and-subagents.md`](../develop/references/config-and-subagents.md) and resolve `medium_effort_model` (default `inherit`) and `delegation_policy` from `develop-config.md`.
   - When `delegation_policy` is not `single-agent` and your coding assistant has a subagent tool, spawn a read-only subagent starting with `Read <develop-dir>/worker.md before anything else.`, followed by [`references/comment-auditor.md`](references/comment-auditor.md) verbatim and the scope. Follow the deprecated-model fallback protocol if a configured model is rejected.
   - If your coding assistant has no subagent tool or `delegation_policy` is `single-agent`, follow [`references/comment-auditor.md`](references/comment-auditor.md) yourself in a dedicated fresh pass over the scope.
2. **Audit the report and prepare proposals.** Reject any application-code edits, out-of-scope suggestions, deletions of protected keep-list exceptions, inaccurate `REFACTOR` claims, or flags against intentional, clear code.
   - Keep `REFACTOR` flags for surprises in our own code. Do not keep explanatory comments that hide confusing local code.
   - Audit missed lint or type suppressions (`eslint-disable`, `@ts-ignore`, `@ts-expect-error`, `# noqa`, `# type: ignore`, `@SuppressWarnings`, and similar directives). Suppressions hiding correctness or safety bugs stay actionable `REFACTOR` items.
   - Before accepting or rejecting thin `IMPORTANT` or `do not remove` claims, trace the named symbol or run **why** on its git history.
   - For constraint comments saying `do not remove`, `do not change wording`, or `talk to X before changing` (outside protected keep-list exceptions), draft the cheapest in-scope structural check (type, runtime assertion, test, or lint rule) to propose in Step 3.
   - Keep `REVIEW` items about unverified external rules intact and report them open to the user.
3. **Confirm before editing (standalone runs).** When invoked directly via `/audit-comments`, present the audited plan (recommended comment deletions, proposed `REFACTOR` root-cause changes, proposed structural checks for constraint comments, and open `REVIEW` items) and wait for user confirmation before editing files. When called as a cleanup step inside an active `/develop` run, you may apply trivial accepted comment deletions directly, while still asking before any non-trivial refactor or new structural check.
4. **Apply approved changes.**
   - Delete only approved filler or narration comments.
   - Fix trivial approved `REFACTOR` items directly (deleting dead paths, dropping unused parameters, calling the real API). If approved `REFACTOR` items require redesigning types or boundaries, run **architect** once for the accepted set before implementing. Apply the smallest root-cause fix inside scope per [Fix Root Causes](../develop/references/principles/fix-root-causes.md) and [Redesign from First Principles](../develop/references/principles/redesign-from-first-principles.md). If the true root cause lies out of scope, land the smallest clean in-scope improvement and report the remainder open. Never add defensive symptom guards.
   - For each approved structural check on a constraint comment, encode the check and delete the superseded comment. If the user declines a proposed structural check, keep the comment untouched unless the user explicitly approves deleting it, and note it open in your report.
5. **Report.** Summarize comments deleted, protected exceptions kept, open `REVIEW` items, approved `REFACTOR` fixes applied, structural checks added or declined, any out-of-scope follow-ups, and any model fallback notice if triggered.
