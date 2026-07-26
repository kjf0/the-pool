---
name: start-coding-day
description: Prepare a git repository for a coding session. Use when the user asks to start a coding day, begin work, resume project development, check leftover work before coding, sync the project before work, or verify a repo/worktree/tooling baseline before making changes.
---

# Start Coding Day

## Overview

Use this skill to establish a clean, explicit starting point before development. Favor diagnosis and safe fast-forwards over clever recovery; surface uncertainty early.

## Workflow

1. Run the helper script from the repository root:

   ```powershell
   python .codex\skills\start-coding-day\scripts\start_day_check.py --repo .
   ```

2. Read the report and identify:

   - Current date in `YYYY-MM-DD HHMM` format.
   - Project folder path, anchor path, and worktrees path.
   - Current branch and upstream.
   - Uncommitted or untracked files.
   - Worktrees and whether they look stale.
   - Remote configuration.
   - Tool visibility for `git`, `node`, `npm`, `pnpm`, and `gh`.
   - Whether local `main` and `origin/main` can be compared.
   - Suggested branch/worktree name for the backlog item when provided.

3. If the user asked to sync before work, or if syncing is clearly part of the requested startup, run:

   ```powershell
   python .codex\skills\start-coding-day\scripts\start_day_check.py --repo . --fetch
   ```

4. If local `main` is checked out, clean, tracks `origin/main`, and can be fast-forwarded, fast-forward it with ordinary git commands. Stop instead of merging if:

   - The worktree has uncommitted changes.
   - `main` and `origin/main` diverged.
   - The repository is not on `main` and switching would disturb local work.
   - Fetch fails or remote state is unclear.

5. Summarize the starting state in plain language:

   - Ready to code.
   - Needs cleanup first.
   - Needs user decision.
   - Blocked by tooling, permissions, conflicts, or remote problems.

## Branch And Worktree Naming

Display dates as:

```text
YYYY-MM-DD HHMM
```

Name branches and worktrees with the same timestamp made git/path-safe:

```text
YYYY-MM-DD_HHMM-backlog_item_short_description
```

Use a short lowercase description derived from the backlog item. Replace spaces and unsafe path characters with hyphens. Example:

```text
2026-07-25_0915-build-three-page-website
```

## Worktree Location

Keep feature worktrees out of the top-level projects folder. By default, use:

```text
<projects-anchor>\worktrees\<project-name>\<branch-name>
```

For this project, use:

```text
E:\users\kjf\Documents\dev\ai\projects\worktrees\the-pool\<branch-name>
```

Do not create one sibling folder per worktree directly under `E:\users\kjf\Documents\dev\ai\projects`. If a developer chooses an in-repo `worktrees\` folder instead, keep it ignored by git.

## Project Notes

For the Poolside project:

- Use `the-pool` as the project-facing name and Codex project name.
- Treat `E:\users\kjf\Documents\dev\ai\projects\the-pool` as the current project folder and anchor checkout.
- Treat `the-pool-new` as a temporary Windows rename recovery name, not the current project.
- Keep website source and plain-Markdown Obsidian notes in the same repository.
- Treat stale PATH as plausible on Windows when Codex cannot find tools that may have been installed after the app started.
- Do not treat missing `npm` or `gh` as definitive until checking known direct paths or asking the user to reload Codex.

## Team Usage

- Treat this repository copy as the shared source of truth for the workflow.
- Keep project workflow skills under `.codex/skills/` so the team can review and version them with code.
- If a developer also installs a personal copy, keep it synchronized with this repo copy.

## Safety Rules

- Do not discard changes, force-push, delete worktrees, or rewrite branches without explicit user approval.
- Do not rename active project folders while Codex is using them.
- Do not update Codex memory unless the user explicitly asks for a memory update.
- Report pre-existing dirty files separately from files changed during the current task.
