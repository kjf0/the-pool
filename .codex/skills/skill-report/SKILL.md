---
name: skill-report
description: Report the repo-owned Codex skills available for The Pool. Use when the user asks for `skill-report`, asks to list repo skills, wants to know which workflow skill to use, audits shared workflow coverage, or compares project skills before adding or updating one.
---

# Skill Report

## Overview

Use this skill to list the project skills under `.codex\skills` with their descriptions and workflow groups. Prefer these repo-owned skills over personal duplicates for The Pool work.

## Workflow

1. Run the helper:

   ```powershell
   python .codex\skills\skill-report\scripts\skill_report.py --repo .
   ```

2. Report:

   - Skill source path.
   - Count of repo-owned skills.
   - Skill names grouped by usage area.
   - One-line description for each skill.
   - Reminder to prefer repo-owned skills.

3. If a skill appears missing or stale:

   - Check `.codex\skills`.
   - Check `notes\shared_skills_strategy.md`.
   - Use the skill-creation workflow only when a new or updated skill is actually needed.

## Safety Rules

- Do not list personal skills as project source of truth.
- Do not create duplicate skills during a report.
- Do not update backlog status unless the report task itself changes project state.
- Keep repo-owned skills under `.codex\skills`.
