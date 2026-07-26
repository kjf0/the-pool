# Backlog

This project was originally `pool-site`, temporarily used `the-pool-new` during Windows rename recovery, and is now anchored at `the-pool`.

- Current project folder: `E:\users\kjf\Documents\dev\ai\projects\the-pool`
- Previous project folder: `E:\users\kjf\Documents\dev\ai\projects\the-pool-old`
- Completed folder cleanup: after logging out and back in, renamed the old `the-pool` folder to `the-pool-old`, renamed `the-pool-new` to `the-pool`, and renamed the Codex project from `the-pool-new` to `the-pool`.

The reboot followed git problems and file permission errors, so workflow reliability is part of the project scope, not just website development.

## Metadata Fields

Each backlog item should include:

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

Expected behavior:

- Check repository status, current branch, worktrees, and remotes.
- Verify development tools are visible to Codex.
- Detect stale PATH issues before treating missing tools as definitive.
- Sync `main` from origin when safe.
- Summarize any leftover work that needs attention before new development starts.

Evidence:

- Created shared repo Codex skill at `.codex\skills\start-coding-day`.
- Added `start_day_check.py` helper script for repeatable repo startup checks.
- Validated the skill successfully.

### 2. Status summary skill

Status: Done
Labels: workflow, codex-skill, reporting, handoff
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-25

Create a Codex skill that reports the current project state at a logical stopping point so work can resume later.

Expected behavior:

- Trigger when the user asks for `status-summary`.
- Summarize current branch, worktree path, open PRs, uncommitted changes, and recently completed work.
- Identify the active backlog item, if any.
- Recommend the next action after a break, including whether to merge PRs, sync `main`, clean up worktrees, or continue coding.
- Include enough context for returning after several hours or overnight.
- Keep the summary concise and durable enough to paste into notes if needed.

Evidence:

- Created shared repo Codex skill at `.codex\skills\status-summary`.
- Added `status_summary.py` helper script for read-only project status reports.
- Verified the helper reports current branch, worktree path, open PRs, backlog context, likely active item, and recommended next action.

### 3. Finish previous work skill

Status: Done
Labels: workflow, codex-skill, git
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-25

Create a Codex skill that cleans up work left from a previous day.

Expected behavior:

- Identify uncommitted changes, unpublished branches, stale worktrees, and incomplete validation.
- Suggest whether to commit, stash, push, archive, or continue the work.
- Avoid deleting worktrees, force-pushing, or discarding changes without explicit approval.

Evidence:

- Created shared repo Codex skill at `.codex\skills\finish-previous-work`.
- Added `finish_previous_work.py` helper script for read-only leftover work audits.
- Verified the helper reports dirty worktrees, branches without upstreams, backlog matches, open PRs, and cleanup recommendations.

### 4. Sync local main skill

Status: Done
Labels: workflow, codex-skill, git
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-25

Create a Codex skill or script-backed workflow to update local `main`.

Expected behavior:

- Fetch origin.
- Confirm the local branch is `main` or switch safely.
- Fast-forward local `main` from `origin/main` when possible.
- Stop and report clearly if local `main` has divergent or uncommitted work.

Evidence:

- Created shared repo Codex skill at `.codex\skills\sync-local-main`.
- Added `sync_local_main.py` helper script for dry-run checks, fetches, and fast-forward-only main updates.
- Verified the helper reports local changes, current branch, fetch status, ahead/behind counts, and safe stop conditions.

### 5. Create feature worktree skill

Status: Done
Labels: workflow, codex-skill, git, worktree
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-25

Create a Codex skill that creates a dedicated worktree and branch from updated `main`.

Expected behavior:

- Update `main` first.
- Create a named worktree in the project worktree area.
- Create a `codex/...` branch unless another prefix is requested.
- Check out the branch in the new worktree.
- Verify dependencies and record the task context.
- Add the exact created worktree path to Git `safe.directory` to avoid Windows dubious ownership warnings.

Evidence:

- Created shared repo Codex skill at `.codex\skills\create-feature-worktree`.
- Added `create_feature_worktree.py` helper script for dry-run previews and safe worktree creation.
- Implemented the shared path policy: `E:\users\kjf\Documents\dev\ai\projects\worktrees\the-pool\<branch-name>`.
- Added exact-path `safe.directory` trust after worktree creation, without broad wildcard trust.

### 6. Modify code workflow

Status: Done
Labels: workflow, codex-skill, development
Priority: P1
Assigned dev: Codex
Estimated code complete: 2026-07-25

Define the normal Codex development loop for this project.

Expected behavior:

- Read existing code and notes before editing.
- Keep website source and Obsidian notes in the same repository.
- Make small, scoped changes.
- Run appropriate validation before publishing.
- Update notes when decisions or workflow lessons should persist.

Evidence:

- Created shared repo Codex skill at `.codex\skills\modify-code-workflow`.
- Added `modify_code_check.py` helper script for pre-edit and post-edit development context reports.
- Documented the normal development loop: gather context, edit narrowly, validate appropriately, and summarize for publishing.

### 7. Sync feature branch with main skill

Status: Not started
Labels: workflow, codex-skill, git
Priority: P1
Assigned dev: Unassigned
Estimated code complete: TBD

Create a Codex skill that updates an active feature branch from current `main`.

Expected behavior:

- Fetch origin and update `main`.
- Rebase or merge according to the chosen project policy.
- Surface conflicts clearly.
- Run validation after the sync completes.

### 8. Publish branch/worktree skill

Status: Done
Labels: workflow, codex-skill, git, github
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-26

Create a Codex skill that prepares and publishes a branch.

Expected behavior:

- Show status and changed files.
- Run build and test checks.
- Stage only intentional files.
- Commit with a clear message.
- Push the branch to origin.

Evidence:

- Created shared repo Codex skill at `.codex\skills\publish-branch-worktree`.
- Added `publish_branch_worktree.py` helper script for dry-run scope review, validation, explicit staging, commit, and push.
- Verified the helper refuses default-branch publishing and requires explicit files or `--all-changes`.
- Validated the skill with `quick_validate.py`.
- Compiled the helper with `python -m py_compile`.

### 9. Create PR skill

Status: Done
Labels: workflow, codex-skill, github
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-26

Create a Codex skill that opens a pull request to `main`.

Expected behavior:

- Use the GitHub remote `kjf0/the-pool`.
- Create a draft PR by default.
- Include a concise summary, validation results, and notes about any known risks.

Evidence:

- Created shared repo Codex skill at `.codex\skills\create-pr`.
- Added `create_pr.py` helper script for PR readiness checks and draft PR creation through `gh`.
- Verified the helper refuses PR creation when the worktree has unpublished local changes.
- Validated the skill with `quick_validate.py`.
- Compiled the helper with `python -m py_compile`.

### 10. Review and merge outside Codex

Status: Not started
Labels: workflow, github, review
Priority: P2
Assigned dev: User
Estimated code complete: TBD

Keep PR review and merge as a separately supervised step outside Codex.

Expected behavior:

- Codex may summarize PRs, check CI, and address review comments.
- Final merge remains a deliberate user action unless the policy changes later.

### 11. Project memory curator skill

Status: Not started
Labels: workflow, codex-skill, memory, notes
Priority: P1
Assigned dev: Unassigned
Estimated code complete: TBD

Create a Codex skill for durable project memory and notes hygiene.

Expected behavior:

- Update repo notes when project decisions are made.
- Add Codex memory update notes only when explicitly requested.
- Keep memory short, evidence-based, and focused on repeatable workflow lessons.

### 12. Shared skills strategy

Status: Not started
Labels: workflow, codex-skill, team
Priority: P1
Assigned dev: Unassigned
Estimated code complete: TBD

Design a way to share Codex workflow skills between projects.

Expected behavior:

- Treat repo-owned skills as the source of truth for project-specific workflows.
- Avoid duplicate personal and repo skill copies that can drift out of sync.
- Decide whether common cross-project skills should live in a dedicated shared skills repository, a plugin, a template, a submodule, or a documented sync/install workflow.
- Define how team members discover, install, update, and validate shared skills.
- Keep project-specific details in the project repo while allowing common workflow code to be reused.

### 13. Skill report skill

Status: Not started
Labels: workflow, codex-skill, reporting
Priority: P1
Assigned dev: Unassigned
Estimated code complete: TBD

Create a Codex skill that reports the repo skills available for the current project.

Expected behavior:

- Trigger when the user asks for `skill-report`.
- List repo skills available under `.codex\skills`.
- Include each skill name.
- Include a short description of what each skill does.
- Include a label for grouping similar skills.
- Prefer repo-owned skills over personal duplicates.
- Make the report useful for a dev team deciding which shared workflow skill to use.

### 14. Backlog item metadata

Status: Done
Labels: backlog, planning, website-data
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-25

Improve the backlog structure so each item can carry planning and ownership metadata.

Expected behavior:

- Add labels to backlog items so similar work can be grouped.
- Add priority to backlog items.
- Add assigned dev to backlog items.
- Add estimated code complete date to backlog items.
- Keep the Markdown backlog easy to edit by hand while making it structured enough for the website backlog page to render.

Evidence:

- Added a metadata field legend.
- Added labels, priority, assigned dev, and estimated code complete fields to all current backlog items.
- Marked item 13 complete after applying the metadata structure.

### 15. Renaming fix

Status: Done
Labels: workflow, codex-skill, rename, project-setup
Priority: P0
Assigned dev: Codex
Estimated code complete: 2026-07-26

Adjust repo workflow notes and Codex skills to use the current project folder name and Codex project name after the Windows rename recovery.

Expected behavior:

- Treat `E:\users\kjf\Documents\dev\ai\projects\the-pool` as the active project folder and anchor checkout.
- Treat `the-pool` as the Codex project name.
- Remove stale guidance that says `the-pool-new` is the current reboot folder.
- Preserve historical context that `the-pool-new` was temporary and `the-pool-old` is the old folder.
- Verify repo-owned skills and helper scripts do not rely on the temporary project name.

Evidence:

- Updated this backlog header to reflect the completed rename from `the-pool-new` to `the-pool`.
- Added explicit `the-pool` project name and anchor folder guidance to `.codex\skills\start-coding-day\SKILL.md`.
- Verified repo-owned skills and helper scripts contain no stale `the-pool-new` current-folder guidance.
- Ran `start_day_check.py` and `status_summary.py`; both report `E:\users\kjf\Documents\dev\ai\projects\the-pool` as the active project folder.

## Website Work

### 16. Build three-page website structure

Status: Not started
Labels: website, backlog, project-page
Priority: P0
Assigned dev: Unassigned
Estimated code complete: TBD

Create the initial website with three pages.

Expected behavior:

- Home: the website's main home page and the primary object of this project.
- Project: a project status and information page.
- Backlog: a page showing backlog items and status, so the project backlog can be viewed in the website during development.
- Keep the website simple enough to evolve while making the project workflow visible.

### 17. Confirm reboot baseline

Status: Not started
Labels: reboot, audit, recovery
Priority: P0
Assigned dev: Unassigned
Estimated code complete: TBD

Establish the current website baseline after the folder reboot.

Expected behavior:

- Inspect the current file tree and git history.
- Confirm whether this reboot should preserve, replace, or recover any files from the previous `the-pool` folder.
- Document what is intentionally carried forward from the old project.

### 18. Define first usable website milestone

Status: Not started
Labels: product, website, planning
Priority: P1
Assigned dev: Unassigned
Estimated code complete: TBD

Define the next product milestone for the Poolside website.

Expected behavior:

- Clarify the first screen and core workflow.
- Identify the minimum useful pool maintenance data model.
- Decide which content belongs in the website and which belongs only in Obsidian notes.

### 19. Editable backlog page with persisted data

Status: Not started
Labels: website, backlog, data-model
Priority: P0
Assigned dev: Unassigned
Estimated code complete: TBD

Give the website backlog page the ability to add and change backlog items.

Expected behavior:

- Move backlog items out of the Markdown file and into a persisted data structure.
- Keep enough structure to support labels, priority, assigned dev, status, estimated code complete date, and item descriptions.
- Let the backlog page create new backlog items.
- Let the backlog page edit existing backlog items.
- Preserve a readable project/backlog report for Codex and human review.
- Decide how Markdown notes should reference or summarize the persisted backlog after migration.
