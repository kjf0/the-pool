
# Architecture

## Reboot Baseline

The current project anchor is `E:\users\kjf\Documents\dev\ai\projects\the-pool`.

The repository currently carries:

- `public_html\` static website files.
- `notes\` plain-Markdown Obsidian project notes.
- `.codex\skills\` repo-owned workflow skills.
- `README.md`.

The website baseline is intentionally simple:

- `public_html\index.html`
- `public_html\project.html`
- `public_html\backlog.html`
- `public_html\styles.css`

No package manager, build system, deployment metadata, or generated assets is part of the current baseline.

Backlog data is stored in `public_html\backlog-data.json`. The website loads this file as seed data and stores browser-local edits in `localStorage`. Repo workflow helpers prefer the JSON data source and fall back to `notes\backlog.md` only when the JSON file is unavailable. Regenerate the Markdown report with `python scripts\sync_backlog_notes.py --apply` after changing the JSON file.

The old recovered folder exists outside this repo at `E:\users\kjf\Documents\dev\ai\projects\the-pool-old`. Nothing is being automatically recovered from it. If old files are needed later, compare them deliberately in a separate backlog item before copying anything forward.
