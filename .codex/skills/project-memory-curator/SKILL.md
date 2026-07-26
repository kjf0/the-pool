---
name: project-memory-curator
description: Curate durable project memory and notes hygiene for The Pool. Use when the user asks to update project memory, capture a workflow lesson, decide whether repo notes or Codex memory should change, maintain notes after a decision, or audit whether backlog/notes updates are needed after project work.
---

# Project Memory Curator

## Overview

Use this skill when a project decision, workflow lesson, or durable context should be recorded. Prefer repo-owned notes and structured backlog data first. Only add personal Codex memory update notes when the user explicitly asks.

## Workflow

1. Run the helper:

   ```powershell
   python .codex\skills\project-memory-curator\scripts\memory_curator_check.py --repo .
   ```

2. Decide the right memory surface:

   - `public_html\backlog-data.json`: structured backlog state.
   - `notes\backlog.md`: generated backlog report; regenerate from JSON instead of editing by hand.
   - `notes\architecture.md`: stable technical baseline and architecture choices.
   - `notes\decision_log.md`: project decisions and rationale.
   - `notes\maintenance_notes.md`: operational lessons and recurring maintenance notes.
   - Personal Codex memory: only when the user explicitly asks for a memory update.

3. If backlog state changes, edit `public_html\backlog-data.json`, then regenerate:

   ```powershell
   python scripts\sync_backlog_notes.py --apply
   python scripts\sync_backlog_notes.py --check
   ```

4. Keep entries short and evidence-based:

   - What changed.
   - Why it matters later.
   - Where the evidence lives.
   - What action future Codex runs should repeat or avoid.

5. Validate:

   - Run `git diff --check`.
   - Run `python scripts\sync_backlog_notes.py --check` after backlog edits.
   - Run syntax checks for edited scripts.

## Safety Rules

- Do not update personal Codex memory unless the user explicitly asks.
- Do not edit generated `notes\backlog.md` directly; update JSON and regenerate it.
- Do not record secrets, credentials, or noisy local state.
- Do not turn temporary guesses into durable memory.
- Keep repo-owned skills and notes in this repository.
