#!/usr/bin/env python3
"""Print a read-only status summary for resuming project work."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


def run(cwd: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def git(repo: Path, *args: str) -> tuple[int, str]:
    result = run(repo, ["git", *args])
    return result.returncode, (result.stdout + result.stderr).rstrip()


def gh(repo: Path, *args: str) -> tuple[int, str]:
    result = run(repo, ["gh", *args])
    return result.returncode, (result.stdout + result.stderr).rstrip()


def section(title: str) -> None:
    print(f"\n## {title}")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


@dataclass
class BacklogItem:
    number: int
    title: str
    status: str = ""
    labels: str = ""
    priority: str = ""
    assigned: str = ""
    estimate: str = ""

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
        for attr, prefix in (
            ("status", "Status: "),
            ("labels", "Labels: "),
            ("priority", "Priority: "),
            ("assigned", "Assigned dev: "),
            ("estimate", "Estimated code complete: "),
        ):
            if line.startswith(prefix):
                setattr(current, attr, line.removeprefix(prefix).strip())
    return items


def current_branch(repo: Path) -> str:
    code, output = git(repo, "branch", "--show-current")
    return output if code == 0 and output else "(detached HEAD)"


def print_key_value(key: str, value: str) -> None:
    print(f"{key}: {value}")


def open_prs(repo: Path) -> tuple[list[dict], str | None]:
    if not shutil.which("gh"):
        return [], "gh not found on PATH"
    code, output = gh(
        repo,
        "pr",
        "list",
        "--state",
        "open",
        "--json",
        "number,title,isDraft,headRefName,baseRefName,url,mergeable",
    )
    if code != 0:
        return [], output or "gh pr list failed"
    try:
        return json.loads(output), None
    except json.JSONDecodeError as exc:
        return [], f"Could not parse gh output: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository or worktree path to summarize.")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    code, root_output = git(repo, "rev-parse", "--show-toplevel")
    if code != 0:
        print(f"Not a git repository: {repo}", file=sys.stderr)
        return 2
    root = Path(root_output).resolve()
    branch = current_branch(root)
    backlog_items = parse_backlog(root / "notes" / "backlog.md")
    prs, pr_error = open_prs(root)

    print("# Status Summary Report")
    print_key_value("Current date", datetime.now().strftime("%Y-%m-%d %H%M"))
    print_key_value("Project folder", str(root))
    print_key_value("Current branch", branch)

    section("Local Git")
    code, status = git(root, "status", "--short", "--branch")
    print(status if status else "(no git status output)")
    code, upstream = git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if code == 0:
        code, counts = git(root, "rev-list", "--left-right", "--count", f"{branch}...{upstream}")
        if code == 0:
            ahead, behind = counts.split()
            print_key_value(f"Compared with {upstream}", f"behind {behind}, ahead {ahead}")
    else:
        print("No upstream configured for current branch.")

    section("Worktrees")
    code, worktrees = git(root, "worktree", "list")
    print(worktrees if code == 0 and worktrees else "(none found)")

    section("Open PRs")
    if pr_error:
        print(f"Could not check PRs: {pr_error}")
    elif prs:
        for pr in prs:
            draft = "draft" if pr.get("isDraft") else "ready"
            print(
                f"#{pr.get('number')} {pr.get('title')} [{draft}] "
                f"{pr.get('headRefName')} -> {pr.get('baseRefName')} "
                f"mergeable={pr.get('mergeable')} {pr.get('url')}"
            )
    else:
        print("(none)")

    section("Backlog")
    done = [item for item in backlog_items if item.status.lower() == "done"]
    next_items = [
        item
        for item in backlog_items
        if item.status.lower() in {"not started", "in progress", "blocked"}
    ]
    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    next_items.sort(key=lambda item: (priority_order.get(item.priority, 9), item.number))
    if done:
        print("Recently/completed:")
        for item in done[-5:]:
            print(f"- {item.number}. {item.title} ({item.priority})")
    if next_items:
        print("Highest-priority remaining:")
        for item in next_items[:5]:
            print(f"- {item.number}. {item.title} ({item.priority}, {item.status})")

    section("Likely Active Item")
    branch_slug = slugify(branch)
    matches = [item for item in backlog_items if item.slug and item.slug in branch_slug]
    if matches:
        for item in matches:
            print(f"{item.number}. {item.title} ({item.status}, {item.priority})")
    else:
        print("No backlog item clearly matches the current branch.")

    section("Recommended Next")
    code, porcelain = git(root, "status", "--porcelain")
    dirty = bool(porcelain.strip())
    if dirty:
        print("Review or publish local changes before switching context.")
    elif prs:
        print("Review open PRs and merge/sync before starting unrelated work.")
    elif branch == "main" and next_items:
        item = next_items[0]
        print(f"Start next item: {item.number}. {item.title} ({item.priority}).")
    elif branch != "main":
        print("Continue this branch or open/update its PR.")
    else:
        print("No specific next action found.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
