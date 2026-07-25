---
name: status-summary
description: Summarize the current project state before a break or after returning to work. Use when the user asks for `status-summary`, asks where they left off, asks what to do next, reaches a logical stopping point, pauses overnight, resumes after time away, or needs a concise handoff report for a repo/worktree/backlog/PR state.
---

# Status Summary

## Overview

Use this skill to create a durable, concise report of where project work stands and what should happen next. Prefer facts from local git, GitHub, worktrees, and the repo backlog over memory or guesswork.

## Workflow

1. Run the helper from the repository or active worktree:

   ```powershell
   python .codex\skills\status-summary\scripts\status_summary.py --repo .
   ```

2. If the helper cannot find `gh`, or GitHub auth is unavailable, still summarize local state and explicitly say GitHub PR state could not be checked.

3. Read the helper output and produce a short human-facing summary with:

   - Current date and time.
   - Current project folder and branch.
   - Clean or dirty working tree.
   - Active worktrees.
   - Open PRs and whether any should be merged before continuing.
   - Recently completed backlog items.
   - Highest-priority not-started backlog items.
   - Likely active backlog item, inferred from branch name when possible.
   - Recommended next action.

4. If there are uncommitted changes, make that the first recommendation. Do not suggest merge, sync, or cleanup before the user understands local changes.

5. If the current branch has an open PR, recommend whether to wait for review/merge, update the PR, or continue work on that branch.

6. If main is clean, aligned with origin, and no PRs are open, recommend the next highest-priority backlog item.

## Output Shape

Keep the final answer brief enough to be useful after an overnight pause. Use this order:

```text
Status:
Where You Are:
Open PRs:
Backlog:
Recommended Next:
```

Use bullets only where they improve scanning.

## Safety Rules

- Do not modify files, stage changes, commit, push, delete branches, remove worktrees, or update memory.
- Do not assume PR state from memory; check GitHub when possible.
- Do not report old PRs as open after `gh pr list` shows none.
- If the repo is dirty, preserve the exact changed-file list in the summary.
