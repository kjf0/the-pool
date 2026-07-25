---
name: sync-local-main
description: Safely update local main from origin/main. Use when the user asks to sync main, update local main, get latest main, proceed after a PR was merged, prepare main before creating a feature worktree, or verify whether local main can be fast-forwarded without losing work.
---

# Sync Local Main

## Overview

Use this skill to bring local `main` up to date with `origin/main` while preserving work. Prefer fast-forward-only updates and clear stops over automatic branch switching or conflict resolution.

## Workflow

1. Run the helper from the active repository or main anchor:

   ```powershell
   python .codex\skills\sync-local-main\scripts\sync_local_main.py --repo . --apply
   ```

2. Read the report before taking any follow-up action. It includes:

   - Current date, repo path, and current branch.
   - Local changed files.
   - Fetch result.
   - `main` compared with `origin/main`.
   - Whether a fast-forward happened or why it stopped.

3. If the helper stops, report the blocker and ask for the next decision only when needed:

   - Dirty local changes: finish, commit, stash by explicit request, or switch context later.
   - Not on `main`: decide whether to return to the main anchor/worktree.
   - Local `main` ahead of or divergent from `origin/main`: inspect commits before merging, rebasing, or publishing.
   - Missing `origin/main`: verify remotes and repository setup.

4. After a successful sync, use the updated `main` as the base for new worktrees and branches.

## Dry Run

Use a dry run when the user asks whether main is safe to sync:

```powershell
python .codex\skills\sync-local-main\scripts\sync_local_main.py --repo .
```

The dry run fetches only when `--fetch` is supplied and never changes branches or commits.

## Safety Rules

- Do not discard changes, stash, reset, force-push, or delete branches.
- Do not switch branches when the current worktree has local changes.
- Do not merge unless it is `git merge --ff-only origin/main` on local `main`.
- Stop when `main` is ahead of or divergent from `origin/main`; report the exact ahead/behind counts.
- Keep repo-owned skills under `.codex\skills`; do not create personal duplicate skills.
