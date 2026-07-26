# Shared Skills Strategy

## Current Decision

Keep The Pool workflow skills in this repository under `.codex\skills`.

This repository is the source of truth for project-specific skills because the skills depend on:

- The project folder and worktree layout.
- The JSON-backed backlog workflow.
- The repo notes conventions.
- The GitHub repository `kjf0/the-pool`.

Do not create personal duplicate skills for this project unless there is a specific reason. Personal copies can drift from the repo copy and make future Codex runs inconsistent.

## Sharing Rule

Use three levels of sharing:

1. Repo-owned skills for The Pool-specific workflow.
2. Copy/paste or documented install from this repo only when another project intentionally wants the same workflow.
3. Extract to a dedicated shared skills repo, plugin, or template only after at least two projects need the same skill with minimal project-specific changes.

## Update Workflow

When a repo-owned skill changes:

1. Edit the skill under `.codex\skills`.
2. Validate the skill with `quick_validate.py`.
3. Run any bundled helper script checks.
4. Update `public_html\backlog-data.json` when backlog status changes.
5. Regenerate `notes\backlog.md` with `python scripts\sync_backlog_notes.py --apply`.
6. Commit, push, and open a PR.

## Team Discovery

Team members should discover project workflow skills from:

- `.codex\skills` for executable skill definitions.
- `notes\backlog.md` for generated backlog status.
- `notes\shared_skills_strategy.md` for sharing policy.

If a future skill becomes reusable across projects, document which parts are generic and which parts must remain project-specific before extracting it.
