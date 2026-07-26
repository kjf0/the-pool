---
name: publish-branch-worktree
description: Prepare and publish a feature branch or worktree by reviewing local changes, running validation, staging intentional files, committing, and pushing to origin. Use when the user asks to publish committed work, push a feature branch, prepare a branch for PR, commit and push current worktree changes, or finish the publish step before PR creation.
---

# Publish Branch Worktree

## Overview

Use this skill after code or notes changes are complete in a feature worktree. Keep the publish step narrow: show the exact scope, run relevant checks, stage only intentional files, commit once with a clear message, and push the current branch.

## Workflow

1. Inspect the current worktree:

   ```powershell
   python .codex\skills\publish-branch-worktree\scripts\publish_branch_worktree.py --repo .
   ```

2. Review the report before staging:

   - Current branch and upstream.
   - Local changed files.
   - Staging plan.
   - Validation plan.
   - Any stop condition.

3. Choose the intentional files. Prefer explicit paths:

   ```powershell
   python .codex\skills\publish-branch-worktree\scripts\publish_branch_worktree.py --repo . --file notes\backlog.md --file .codex\skills\example\SKILL.md
   ```

   Use `--all-changes` only when every local change belongs to the publish scope.

4. Add validation commands with repeated `--check` arguments when the default `git diff --check` is not enough:

   ```powershell
   python .codex\skills\publish-branch-worktree\scripts\publish_branch_worktree.py --repo . --file notes\backlog.md --check "git diff --check" --check "python C:\Users\kjf\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\example"
   ```

5. Publish only after the dry run shows the intended scope:

   ```powershell
   python .codex\skills\publish-branch-worktree\scripts\publish_branch_worktree.py --repo . --file notes\backlog.md --message "Describe the change" --apply
   ```

6. Summarize:

   - Branch name.
   - Commit hash and message.
   - Push target.
   - Validation commands and results.
   - Whether the branch is ready for the create-PR skill.

## Helper Behavior

The helper script:

- Refuses to publish from `main` or `master`.
- Refuses detached HEAD.
- Refuses to continue without local changes.
- Requires explicit `--file` paths unless `--all-changes` is supplied.
- Requires `--message` with `--apply`.
- Runs validation before staging and committing.
- Uses `git push -u origin <branch>` when no upstream exists.

## Safety Rules

- Do not stage unrelated files.
- Do not publish directly from the main anchor checkout.
- Do not amend, reset, rebase, force-push, delete branches, or delete worktrees.
- Stop if validation fails and report the failing command.
- Keep repo-owned skills under `.codex\skills`; do not create personal duplicate skills.
