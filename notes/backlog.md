# Backlog

This file is generated from `public_html\backlog-data.json`.

Edit the JSON file first, then run:

```powershell
python scripts\sync_backlog_notes.py --apply
```

Use this check before publishing backlog changes:

```powershell
python scripts\sync_backlog_notes.py --check
```

## Project Context

This project was originally `pool-site`, temporarily used `the-pool-new` during Windows rename recovery, and is now anchored at `the-pool`.

- Current project folder: `E:\users\kjf\Documents\dev\ai\projects\the-pool`
- Previous project folder: `E:\users\kjf\Documents\dev\ai\projects\the-pool-old`
- Completed folder cleanup: after logging out and back in, renamed the old `the-pool` folder to `the-pool-old`, renamed `the-pool-new` to `the-pool`, and renamed the Codex project from `the-pool-new` to `the-pool`.

The reboot followed git problems and file permission errors, so workflow reliability is part of the project scope, not just website development.

## Metadata Fields

Each backlog item includes:

- Status: `Not started`, `In progress`, `Done`, or `Blocked`
- Labels: comma-separated grouping labels
- Priority: `P0`, `P1`, `P2`, or `P3`
- Assigned dev: person or role responsible for code completion
- Estimated code complete: `YYYY-MM-DD` or `TBD`

## Workflow And Codex Skills

### 1. Start coding day skill

Status: Done
Labels: workflow, codex-skill, git
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-25

Create a Codex skill that prepares the project for a workday of coding.

### 2. Status summary skill

Status: Done
Labels: workflow, codex-skill, reporting, handoff
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-25

Create a Codex skill that reports the current project state at a logical stopping point so work can resume later.

### 3. Finish previous work skill

Status: Done
Labels: workflow, codex-skill, git
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-25

Create a Codex skill that cleans up work left from a previous day.

### 4. Sync local main skill

Status: Done
Labels: workflow, codex-skill, git
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-25

Create a Codex skill or script-backed workflow to update local main.

### 5. Create feature worktree skill

Status: Done
Labels: workflow, codex-skill, git, worktree
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-25

Create a Codex skill that creates a dedicated worktree and branch from updated main.

### 6. Modify code workflow

Status: Done
Labels: workflow, codex-skill, development
Priority: P1
Assigned dev: Codex
Estimated code complete: 2026-07-25

Define the normal Codex development loop for this project.

### 7. Sync feature branch with main skill

Status: Done
Labels: workflow, codex-skill, git
Priority: P1
Assigned dev: Codex
Estimated code complete: 2026-07-26

Create a Codex skill that updates an active feature branch from current main.

### 8. Publish branch/worktree skill

Status: Done
Labels: workflow, codex-skill, git, github
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-26

Create a Codex skill that prepares and publishes a branch.

### 9. Create PR skill

Status: Done
Labels: workflow, codex-skill, github
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-26

Create a Codex skill that opens a pull request to main.

### 10. Review and merge outside Codex

Status: Not started
Labels: workflow, github, review
Priority: P2
Assigned dev: User
Estimated code complete: TBD

Keep PR review and merge as a separately supervised step outside Codex.

### 11. Project memory curator skill

Status: Done
Labels: workflow, codex-skill, memory, notes
Priority: P1
Assigned dev: Codex
Estimated code complete: 2026-07-26

Create a Codex skill for durable project memory and notes hygiene.

### 12. Shared skills strategy

Status: Done
Labels: workflow, codex-skill, team
Priority: P1
Assigned dev: Codex
Estimated code complete: 2026-07-26

Keep repo-owned skills as the project source of truth and define when reusable skills should be copied, documented, or extracted.

### 13. Skill report skill

Status: Done
Labels: workflow, codex-skill, reporting
Priority: P1
Assigned dev: Codex
Estimated code complete: 2026-07-26

Create a Codex skill that reports the repo skills available for the current project.

### 14. Backlog item metadata

Status: Done
Labels: backlog, planning, website-data
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-25

Improve the backlog structure so each item can carry planning and ownership metadata.

### 15. Renaming fix

Status: Done
Labels: workflow, codex-skill, rename, project-setup
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-26

Adjust repo workflow notes and Codex skills to use the current project folder name and Codex project name after Windows rename recovery.

## Website Work

### 16. Build three-page website structure

Status: Done
Labels: website, backlog, project-page
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-26

Create the initial home, project, and backlog pages for the website.

### 17. Confirm reboot baseline

Status: Done
Labels: reboot, audit, recovery
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-26

Establish the current website baseline after the folder reboot.

### 18. Define first usable website milestone

Status: Done
Labels: product, website, planning
Priority: P1
Assigned dev: Codex
Estimated code complete: 2026-07-27

Define the first useful website milestone as a browser-local pool care log with readings, tasks, and notes.

### 19. Editable backlog page with persisted data

Status: Done
Labels: website, backlog, data-model
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-26

Use repo-backed JSON as the structured backlog source, regenerate the Markdown backlog report from it, and let the website backlog page add and change browser-local backlog items.
