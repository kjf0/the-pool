#!/usr/bin/env python3
"""Report project development context before or after code edits."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


def run(cwd: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def git(repo: Path, *args: str) -> tuple[int, str]:
    result = run(repo, ["git", *args])
    return result.returncode, (result.stdout + result.stderr).rstrip()


def section(title: str) -> None:
    print(f"\n## {title}")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def repo_root(repo: Path) -> Path:
    code, output = git(repo, "rev-parse", "--show-toplevel")
    if code != 0:
        raise RuntimeError(output or f"Not a git repository: {repo}")
    return Path(output).resolve()


def current_branch(root: Path) -> str:
    code, output = git(root, "branch", "--show-current")
    if code != 0:
        return ""
    return output.strip()


@dataclass
class BacklogItem:
    number: int
    title: str
    status: str = ""
    priority: str = ""

    @property
    def slug(self) -> str:
        return slugify(self.title)


def parse_backlog(path: Path) -> list[BacklogItem]:
    if not path.exists():
        return []
    items: list[BacklogItem] = []
    current: BacklogItem | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^###\s+(\d+)\.\s+(.+)$", line)
        if match:
            current = BacklogItem(number=int(match.group(1)), title=match.group(2).strip())
            items.append(current)
            continue
        if not current:
            continue
        if line.startswith("Status: "):
            current.status = line.removeprefix("Status: ").strip()
        elif line.startswith("Priority: "):
            current.priority = line.removeprefix("Priority: ").strip()
    return items


def parse_backlog_json(path: Path) -> list[BacklogItem]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    items: list[BacklogItem] = []
    for entry in data:
        items.append(
            BacklogItem(
                number=int(entry.get("id", 0)),
                title=str(entry.get("title", "")).strip(),
                status=str(entry.get("status", "")).strip(),
                priority=str(entry.get("priority", "")).strip(),
            )
        )
    return [item for item in items if item.number and item.title]


def load_backlog(root: Path) -> list[BacklogItem]:
    json_items = parse_backlog_json(root / "public_html" / "backlog-data.json")
    if json_items:
        return json_items
    return parse_backlog(root / "notes" / "backlog.md")


def validation_hints(root: Path) -> list[str]:
    hints: list[str] = []
    if (root / "package.json").exists():
        hints.extend(["npm test", "npm run build"])
    if list(root.rglob("*.py")):
        hints.append("python -m py_compile <changed-python-files>")
    if (root / "public_html" / "index.html").exists():
        hints.append("Inspect public_html/index.html in a browser after frontend changes.")
    return hints


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository or worktree path to inspect.")
    args = parser.parse_args()

    try:
        root = repo_root(Path(args.repo).resolve())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    branch = current_branch(root)
    code, status = git(root, "status", "--short")
    dirty = bool(status.strip()) if code == 0 else True
    backlog_items = load_backlog(root)
    branch_slug = slugify(branch)
    matches = [item for item in backlog_items if item.slug and item.slug in branch_slug]

    print("# Modify Code Workflow Check")
    print(f"Repository: {root}")
    print(f"Current branch: {branch or '(detached HEAD)'}")

    section("Local Changed Files")
    print(status if status.strip() else "(none)")

    section("Likely Backlog Item")
    if matches:
        for item in matches:
            print(f"- {item.number}. {item.title} ({item.status}, {item.priority})")
    else:
        print("(none inferred from branch name)")

    section("Validation Hints")
    hints = validation_hints(root)
    if hints:
        for hint in hints:
            print(f"- {hint}")
    else:
        print("- No project-specific validation commands detected; inspect touched files for appropriate checks.")

    section("Recommended Next")
    if branch == "main":
        print("Create or switch to a feature worktree before editing.")
    elif dirty:
        print("Continue or validate the current local changes before switching context.")
    else:
        print("Gather context for the active backlog item, then make a narrow change.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
