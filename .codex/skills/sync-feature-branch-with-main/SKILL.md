---
name: sync-feature-branch-with-main
description: Update an active feature branch from current main by fetching origin, fast-forwarding local main when safe, and merging main into the feature branch. Use when the user asks to sync a feature branch with main, update a worktree after main changed, refresh a branch before publishing, or resolve branch drift before continuing development.
---

# Sync Feature Branch With Main

## Overview

Use this skill from a feature worktree after `main` has changed or before publishing a long-running branch. Keep the operation conservative: clean worktree only, fast-forward local main only, then merge `main` into the feature branch and report conflicts clearly.

## Workflow

1. Run a dry run from the feature worktree:

   ```powershell
   python .codex\skills\sync-feature-branch-with-main\scripts\sync_feature_branch_with_main.py --repo .
   ```

2. Confirm the report shows:

   - Current branch is a feature branch, not `main`.
   - The feature worktree has no local changes.
   - `main` and `origin/main` can be compared.
   - Local `main` has no unpublished commits.
   - The feature branch comparison with `main` is understood.

3. Apply the sync:

   ```powershell
   python .codex\skills\sync-feature-branch-with-main\scripts\sync_feature_branch_with_main.py --repo . --apply
   ```

4. If the merge succeeds, run validation for the active work before publishing.

5. If conflicts happen, stop and report:

   - Files with conflicts.
   - Whether `main` fast-forwarded successfully first.
   - The exact command that failed.
   - That the user must resolve conflicts or ask Codex to do so before publishing.

## Helper Behavior

The helper script:

- Refuses detached HEAD.
- Refuses to run from `main` or `master`.
- Refuses dirty feature worktrees.
- Fetches `origin --prune` by default with `--apply`.
- Refuses when local `main` is ahead of `origin/main`.
- Fast-forwards local `main` from `origin/main` when needed.
- Merges `main` into the current feature branch with `--no-edit`.

## Safety Rules

- Do not rebase unless the project policy changes.
- Do not force-push.
- Do not stash, discard, or reset local changes.
- Do not resolve conflicts silently.
- Do not publish until the branch is synced and validation has run.
- Keep repo-owned skills under `.codex\skills`; do not create personal duplicate skills.
