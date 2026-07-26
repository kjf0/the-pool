---
name: create-pr
description: Open a GitHub pull request for a clean, already-pushed feature branch. Use when the user asks to create a PR, open a draft PR, prepare a branch for review, make a pull request to main, or complete the PR step after publishing a branch/worktree.
---

# Create PR

## Overview

Use this skill after a feature branch has been committed and pushed. Prefer draft PRs by default, include enough context for review, and leave the final merge as a deliberate user action.

## Workflow

1. Inspect PR readiness:

   ```powershell
   python .codex\skills\create-pr\scripts\create_pr.py --repo .
   ```

2. Confirm the report shows:

   - Current branch is a feature branch, not `main`.
   - Worktree has no local changes.
   - Branch has an upstream.
   - Base branch is correct, normally `main`.
   - The body preview is accurate.

3. Prefer a real Markdown body when there are several details:

   ```powershell
   python .codex\skills\create-pr\scripts\create_pr.py --repo . --title "Add feature" --body-file pr-body.md --apply
   ```

4. For small changes, generate the body from CLI fields:

   ```powershell
   python .codex\skills\create-pr\scripts\create_pr.py --repo . --title "Add feature" --summary "Add the workflow helper." --validation "git diff --check" --validation "npm test" --risk "No known risks." --apply
   ```

5. Create draft PRs by default. Add `--ready` only when the user explicitly asks for a ready-for-review PR.

6. Summarize:

   - PR URL.
   - Branch and base.
   - Draft or ready state.
   - Validation included in the PR body.
   - Any known risks.

## Helper Behavior

The helper script:

- Uses the GitHub CLI `gh`.
- Defaults the base branch from `gh repo view`, falling back to `main`.
- Refuses detached HEAD.
- Refuses PRs from `main`, `master`, or the selected base branch.
- Refuses to create a PR when the worktree has local changes.
- Refuses to create a PR when the branch has no upstream.
- Requires `--title` with `--apply`.
- Writes the PR body through a temporary Markdown file so GitHub renders real newlines.

## Safety Rules

- Do not create a PR before publishing the branch.
- Do not merge PRs unless the project policy changes and the user explicitly asks.
- Do not mark PRs ready for review unless explicitly requested.
- Do not update PRs for unrelated branches.
- Keep repo-owned skills under `.codex\skills`; do not create personal duplicate skills.
