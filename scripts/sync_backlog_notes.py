#!/usr/bin/env python3
"""Regenerate notes/backlog.md from public_html/backlog-data.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


HEADER = """# Backlog

This file is generated from `public_html\\backlog-data.json`.

Edit the JSON file first, then run:

```powershell
python scripts\\sync_backlog_notes.py --apply
```

Use this check before publishing backlog changes:

```powershell
python scripts\\sync_backlog_notes.py --check
```

## Project Context

This project was originally `pool-site`, temporarily used `the-pool-new` during Windows rename recovery, and is now anchored at `the-pool`.

- Current project folder: `E:\\users\\kjf\\Documents\\dev\\ai\\projects\\the-pool`
- Previous project folder: `E:\\users\\kjf\\Documents\\dev\\ai\\projects\\the-pool-old`
- Completed folder cleanup: after logging out and back in, renamed the old `the-pool` folder to `the-pool-old`, renamed `the-pool-new` to `the-pool`, and renamed the Codex project from `the-pool-new` to `the-pool`.

The reboot followed git problems and file permission errors, so workflow reliability is part of the project scope, not just website development.

## Metadata Fields

Each backlog item includes:

- Status: `Not started`, `In progress`, `Done`, or `Blocked`
- Labels: comma-separated grouping labels
- Priority: `P0`, `P1`, `P2`, or `P3`
- Assigned dev: person or role responsible for code completion
- Estimated code complete: `YYYY-MM-DD` or `TBD`
"""


def repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / ".git").exists() or (path / "public_html" / "backlog-data.json").exists():
            return path
    raise RuntimeError(f"Could not find repository root from {start}")


def load_items(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Backlog data must be a list")
    return sorted(data, key=lambda item: int(item["id"]))


def item_section(item: dict) -> str:
    item_id = int(item["id"])
    if item_id >= 16:
        return "Website Work"
    return "Workflow And Codex Skills"


def render_item(item: dict) -> str:
    item_id = int(item["id"])
    title = item["title"]
    lines = [
        f"### {item_id}. {title}",
        "",
        f"Status: {item.get('status', '')}",
        f"Labels: {item.get('labels', '')}",
        f"Priority: {item.get('priority', '')}",
        f"Assigned dev: {item.get('assignedDev', '')}",
        f"Estimated code complete: {item.get('estimatedCodeComplete', '')}",
        "",
        str(item.get("description", "")).strip(),
        "",
    ]
    return "\n".join(lines)


def render(items: list[dict]) -> str:
    sections: dict[str, list[dict]] = {
        "Workflow And Codex Skills": [],
        "Website Work": [],
    }
    for item in items:
        sections.setdefault(item_section(item), []).append(item)

    parts = [HEADER.rstrip(), ""]
    for section, section_items in sections.items():
        if not section_items:
            continue
        parts.append(f"## {section}")
        parts.append("")
        for item in section_items:
            parts.append(render_item(item).rstrip())
            parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository path.")
    parser.add_argument("--apply", action="store_true", help="Rewrite notes/backlog.md.")
    parser.add_argument("--check", action="store_true", help="Fail if notes/backlog.md is out of date.")
    args = parser.parse_args()

    if args.apply and args.check:
        print("Use either --apply or --check, not both.", file=sys.stderr)
        return 2

    root = repo_root(Path(args.repo).resolve())
    data_path = root / "public_html" / "backlog-data.json"
    notes_path = root / "notes" / "backlog.md"
    rendered = render(load_items(data_path))

    if args.check:
        current = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""
        if current != rendered:
            print("notes/backlog.md is out of date. Run scripts\\sync_backlog_notes.py --apply.")
            return 1
        print("notes/backlog.md is in sync.")
        return 0

    if args.apply:
        notes_path.write_text(rendered, encoding="utf-8")
        print(f"Regenerated {notes_path}")
        return 0

    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
