---
name: finish-previous-work
description: Inspect and safely clean up leftover work from a previous coding session. Use when the user asks to finish previous work, clean up yesterday's work, resume after an interruption, handle uncommitted changes, inspect stale worktrees or unpublished branches, decide whether to commit/stash/push/archive, or prepare a project to start fresh work.
---

# Finish Previous Work

## Overview

Use this skill to turn messy leftover repo state into a clear next action. Favor evidence and explicit user decisions over automatic cleanup.

## Workflow

1. Run the helper from the active repository or main anchor:

   ```powershell
   python .codex\skills\finish-previous-work\scripts\finish_previous_work.py --repo .
   ```

2. Read the report and identify:

   - Dirty worktrees and exact changed files.
   - Branches ahead of or behind their upstreams.
   - Local branches without upstreams.
   - Open PRs.
   - Worktrees whose branches are already merged into `main`.
   - Likely active backlog items inferred from branch names.

3. Recommend one of these outcomes:

   - Continue active work.
   - Commit and push intentional changes.
   - Open or update a draft PR.
   - Merge/review an open PR outside Codex.
   - Sync `main`.
   - Remove a clean merged worktree.
   - Stash only after the user explicitly chooses that.
   - Stop for a user decision.

4. If there are local changes, report them first and do not move, delete, or switch worktrees until the user chooses how to handle them.

5. If a worktree branch is merged and clean, it may be removed only after confirming the branch is merged into current `main`.

6. If a branch is ahead of its upstream or has no upstream, do not delete it. Recommend publishing or explicitly archiving it.

## Output Shape

Use this order in the final response:

```text
Findings:
Recommended Cleanup:
Ready For New Work:
```

Keep it short enough to act on immediately.

## Safety Rules

- Do not discard changes, delete worktrees, delete branches, stash, commit, push, rebase, or merge unless the user explicitly asks after seeing the report.
- Do not use `git reset --hard` or checkout files to discard changes.
- Treat untracked files as user work until proven otherwise.
- Keep repo-owned skills under `.codex\skills`; do not create personal duplicate skills.
