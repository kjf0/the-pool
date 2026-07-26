---
name: modify-code-workflow
description: Guide normal project development from context gathering through scoped edits and validation. Use when the user asks Codex to modify code, build a feature, fix a bug, update project notes while coding, continue an active backlog item, or decide what checks to run before publishing work.
---

# Modify Code Workflow

## Overview

Use this skill for the everyday development loop after a feature worktree exists. Keep changes scoped to the active backlog item, read the repo before editing, and leave enough evidence that another developer can review or continue the work.

## Workflow

1. Start with a local state report:

   ```powershell
   python .codex\skills\modify-code-workflow\scripts\modify_code_check.py --repo .
   ```

2. Confirm the active worktree and backlog item:

   - Work from a feature branch/worktree, not the main anchor.
   - Prefer branch names that include the backlog item slug.
   - If the branch and requested work do not match, pause and name the mismatch.

3. Gather context before editing:

   - Read nearby code and notes that own the behavior being changed.
   - Check `notes\backlog.md` for acceptance criteria and related items.
   - Inspect project tooling before inventing validation commands.
   - Preserve unrelated user changes.

4. Edit narrowly:

   - Keep the change focused on the active backlog item.
   - Follow existing file structure and style.
   - Update repo notes when a project decision or workflow lesson should persist.
   - Keep website source and the `notes\` vault in the same repository.

5. Validate at the right level:

   - Run fast syntax or static checks for touched scripts.
   - Run project build/test commands when app behavior changes and tools are available.
   - For visual/frontend work, start the local server when needed and inspect the page before calling it done.
   - If a check cannot run, record why.

6. End with a publish-ready summary:

   - Changed files and intent.
   - Validation commands and results.
   - Known risks or follow-up work.
   - Whether the branch is ready for the publish/PR workflow.

## Safety Rules

- Do not discard, overwrite, or revert changes you did not make.
- Do not commit, push, or open a PR unless the user asks or the active workflow calls for publishing.
- Do not make broad refactors while implementing a narrow backlog item.
- Do not update personal Codex memory unless the user explicitly asks.
- Keep repo-owned skills under `.codex\skills`; do not create personal duplicate skills.
