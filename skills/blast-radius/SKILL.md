---
name: blast-radius
description: "Find hidden downstream breakage beyond a diff and prove the core safety assumption by running real code. Defaults to your current branch diff, or pass a file, commit, PR, or topic after /blast-radius."
disable-model-invocation: true
---

# Blast radius

Find what a change breaks somewhere else before it ships.

Companion to `how` and `why`. `how` tells you what the code does. `why` tells you why it is shaped that way. Blast radius tells you what it breaks somewhere else.

Listing the callers is not the job. Anyone can grep those in a second. The job is the breakage grep will not show you.

## Scope

Use the files, commit, PR, or change the user names. Otherwise default to the current branch diff against the repository's default branch (including uncommitted working-tree changes). If there is no named target and the diff is empty, ask the user what change they want analyzed.

## Do not trust your own writeup

A blast-radius writeup that sounds right is worthless on its own because prose reads as convincing whether or not it is true. Find the one or two facts safety depends on and prove them by running code.

### How sure are you

For each fact the change's safety depends on, push it as far down this list as is practical, and state where it stopped:

1. You said so. Worthless on its own.
2. You pointed at the line. A real `file:line`, or the library's own source.
3. You showed the bad case cannot happen. You walked the failure step by step and it cannot reach.
4. You ran it. A script or test that calls the real code and fails loud if you are wrong.
5. You reproduced it in the running app.

Step 4 is usually one small script that imports the same library the app ships and calls the exact function you are worried about.

## Steps

1. **Read the change.** Inspect the diff, the symbols it adds, changes, and deletes, and what it now does differently (including behavior the diff does not spell out). If a PR exists, also read its description and commits.
2. **Find the core safety fact.** Most changes that look risky are safe because of a single fact, such as "this call only drops already-dead cache entries and does nothing else." Find that fact. If it holds, most risky cases clear at once. Spend your time here instead of listing speculative maybes.
3. **Look where grep stops.** Read the source of any library you call, and check its pinned version and any local patches. Trace runtime ordering and boundaries: event loops, background threads, lifecycle teardown, UI versus worker threads, plugin discovery, serialized formats (JSON, binary, database columns), another language reading the same data, feature flags, and code three hops downstream.
4. **Be honest about each risk.** Give each risk a realistic chance of happening and a concrete impact. Keep confirmed risks and list checked-and-cleared items separately. Cite a real `file:line`. A search that finds nothing is still an answer. Never fabricate a caller or API.
5. **Prove the core safety fact.** Write a focused script or test in a temporary directory (or clean it up afterward unless promoted into the test suite), run it against the real code, and record the output.
6. **Optional multi-perspective check.** For a wide or high-stakes change, offer to run **arena** to compare multiple independent blast-radius analyses. Check `delegation_policy` in `develop-config.md` per [`../develop/references/config-and-subagents.md`](../develop/references/config-and-subagents.md); under `single-agent`, ask the user first and note the parallel token cost before spawning subagents.

## What to hand back

- **What it does.** What changed, including behavior that is not obvious from the diff alone.
- **Core safety fact.** State it, say which confidence step (1 to 5) you reached, and show the proof. If you could not prove it, mark it unproven.
- **Risks.** For each confirmed risk: how it breaks, `file:line`, likelihood and impact, how to check, and proof output for material risks.
- **Cleared.** What you checked and why it is safe.
- **Before you merge.** The cheapest test or reproduction that catches the real bug, including any script you wrote.

Run your writeup through **unslop**, cite real code, and remove any sensitive or private data before posting publicly.

**Reply:** the writeup above, with the core safety fact either proven or marked unproven.
