# Backlog

This project was originally `pool-site`, then renamed to `the-pool`. It is being rebooted again from the current folder:

- Current reboot folder: `E:\users\kjf\Documents\dev\ai\projects\the-pool-new`
- Previous project folder: `E:\users\kjf\Documents\dev\ai\projects\the-pool`
- Intended folder cleanup: rename the previous `the-pool` folder to `the-pool-bad`, then rename `the-pool-new` to `the-pool`

The reboot followed git problems and file permission errors, so workflow reliability is part of the project scope, not just website development.

## Workflow And Codex Skills

### 1. Start coding day skill

Status: Done

Create a Codex skill that prepares the project for a workday of coding.

Expected behavior:

- Check repository status, current branch, worktrees, and remotes.
- Verify development tools are visible to Codex.
- Detect stale PATH issues before treating missing tools as definitive.
- Sync `main` from origin when safe.
- Summarize any leftover work that needs attention before new development starts.

Evidence:

- Created personal Codex skill at `C:\Users\kjf\.codex\skills\start-coding-day`.
- Added `start_day_check.py` helper script for repeatable repo startup checks.
- Validated the skill successfully.

### 2. Finish previous work skill

Create a Codex skill that cleans up work left from a previous day.

Expected behavior:

- Identify uncommitted changes, unpublished branches, stale worktrees, and incomplete validation.
- Suggest whether to commit, stash, push, archive, or continue the work.
- Avoid deleting worktrees, force-pushing, or discarding changes without explicit approval.

### 3. Sync local main skill

Create a Codex skill or script-backed workflow to update local `main`.

Expected behavior:

- Fetch origin.
- Confirm the local branch is `main` or switch safely.
- Fast-forward local `main` from `origin/main` when possible.
- Stop and report clearly if local `main` has divergent or uncommitted work.

### 4. Create feature worktree skill

Create a Codex skill that creates a dedicated worktree and branch from updated `main`.

Expected behavior:

- Update `main` first.
- Create a named worktree in the project worktree area.
- Create a `codex/...` branch unless another prefix is requested.
- Check out the branch in the new worktree.
- Verify dependencies and record the task context.

### 5. Modify code workflow

Define the normal Codex development loop for this project.

Expected behavior:

- Read existing code and notes before editing.
- Keep website source and Obsidian notes in the same repository.
- Make small, scoped changes.
- Run appropriate validation before publishing.
- Update notes when decisions or workflow lessons should persist.

### 6. Sync feature branch with main skill

Create a Codex skill that updates an active feature branch from current `main`.

Expected behavior:

- Fetch origin and update `main`.
- Rebase or merge according to the chosen project policy.
- Surface conflicts clearly.
- Run validation after the sync completes.

### 7. Publish branch/worktree skill

Create a Codex skill that prepares and publishes a branch.

Expected behavior:

- Show status and changed files.
- Run build and test checks.
- Stage only intentional files.
- Commit with a clear message.
- Push the branch to origin.

### 8. Create PR skill

Create a Codex skill that opens a pull request to `main`.

Expected behavior:

- Use the GitHub remote `kjf0/the-pool`.
- Create a draft PR by default.
- Include a concise summary, validation results, and notes about any known risks.

### 9. Review and merge outside Codex

Keep PR review and merge as a separately supervised step outside Codex.

Expected behavior:

- Codex may summarize PRs, check CI, and address review comments.
- Final merge remains a deliberate user action unless the policy changes later.

### 10. Project memory curator skill

Create a Codex skill for durable project memory and notes hygiene.

Expected behavior:

- Update repo notes when project decisions are made.
- Add Codex memory update notes only when explicitly requested.
- Keep memory short, evidence-based, and focused on repeatable workflow lessons.

## Website Work

### 11. Build three-page website structure

Create the initial website with three pages.

Expected behavior:

- Home: the website's main home page and the primary object of this project.
- Project: a project status and information page.
- Backlog: a page showing backlog items and status, so the project backlog can be viewed in the website during development.
- Keep the website simple enough to evolve while making the project workflow visible.

### 12. Confirm reboot baseline

Establish the current website baseline after the folder reboot.

Expected behavior:

- Inspect the current file tree and git history.
- Confirm whether this reboot should preserve, replace, or recover any files from the previous `the-pool` folder.
- Document what is intentionally carried forward from the old project.

### 13. Define first usable website milestone

Define the next product milestone for the Poolside website.

Expected behavior:

- Clarify the first screen and core workflow.
- Identify the minimum useful pool maintenance data model.
- Decide which content belongs in the website and which belongs only in Obsidian notes.
