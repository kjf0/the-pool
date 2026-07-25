---
name: create-feature-worktree
description: Create a dedicated feature worktree and branch from updated main. Use when the user asks to start a backlog item, create a feature worktree, create a worktree/branch, begin new development after syncing main, or prepare an isolated Codex workspace for a project task.
---

# Create Feature Worktree

## Overview

Use this skill to create one clean worktree per backlog item. The worktree path must stay outside the project anchor checkout and under the shared project worktree area.

## Workflow

1. Sync local `main` first:

   ```powershell
   python .codex\skills\sync-local-main\scripts\sync_local_main.py --repo . --apply
   ```

2. Create the feature worktree:

   ```powershell
   python .codex\skills\create-feature-worktree\scripts\create_feature_worktree.py --repo . --backlog-item "short backlog item title" --apply
   ```

3. Use the report to confirm:

   - Current date and generated name.
   - Branch name.
   - Worktree path.
   - Whether `main` was clean and aligned with `origin/main`.
   - Whether the exact worktree path was added to Git `safe.directory`.
   - Next command to enter the new worktree.

## Naming

Use `<YYYY-MM-DD_HHMM>-<backlog-item-short-description>` for the worktree folder. Use `codex/<YYYY-MM-DD_HHMM>-<backlog-item-short-description>` for the branch unless the user requests another branch name.

Default path:

```text
E:\users\kjf\Documents\dev\ai\projects\worktrees\the-pool\<branch-name-without-codex-prefix>
```

## Dry Run

Use a dry run to preview the names and safety checks without creating anything:

```powershell
python .codex\skills\create-feature-worktree\scripts\create_feature_worktree.py --repo . --backlog-item "short backlog item title"
```

## Safety Rules

- Do not create a worktree unless local `main` exists, is clean, and is aligned with `origin/main`.
- Do not create worktrees directly under `E:\users\kjf\Documents\dev\ai\projects`.
- Do not trust broad paths or wildcards. Add only the exact created worktree path to `safe.directory`.
- Do not overwrite an existing branch or worktree folder.
- Stop and report clearly if the generated branch or path already exists.
- Keep repo-owned skills under `.codex\skills`; do not create personal duplicate skills.
