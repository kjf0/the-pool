#!/usr/bin/env python3
"""Audit leftover git work and recommend safe cleanup actions."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
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
    priority: str = ""

    @property
    def slug(self) -> str:
        return slugify(self.title)


@dataclass
class Worktree:
    path: Path
    head: str = ""
    branch_ref: str = ""
    branch: str = ""
    status: str = ""
    upstream: str = ""
    ahead: int | None = None
    behind: int | None = None
    merged: bool | None = None
    backlog_matches: list[BacklogItem] = field(default_factory=list)

    @property
    def dirty(self) -> bool:
        return bool(self.status.strip())


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


def repo_root(repo: Path) -> Path:
    code, output = git(repo, "rev-parse", "--show-toplevel")
    if code != 0:
        raise RuntimeError(output or f"Not a git repository: {repo}")
    return Path(output).resolve()


def parse_worktrees(root: Path) -> list[Worktree]:
    code, output = git(root, "worktree", "list", "--porcelain")
    if code != 0:
        return []
    worktrees: list[Worktree] = []
    current: Worktree | None = None
    for line in output.splitlines():
        if line.startswith("worktree "):
            current = Worktree(path=Path(line.removeprefix("worktree ")).resolve())
            worktrees.append(current)
        elif current and line.startswith("HEAD "):
            current.head = line.removeprefix("HEAD ")
        elif current and line.startswith("branch "):
            current.branch_ref = line.removeprefix("branch ")
            current.branch = current.branch_ref.removeprefix("refs/heads/")
    return worktrees


def fill_worktree_state(worktree: Worktree, main_root: Path, backlog_items: list[BacklogItem]) -> None:
    if not worktree.path.exists():
        worktree.status = "(missing path)"
        return
    code, status = git(worktree.path, "status", "--short")
    worktree.status = status if code == 0 else status or "(status failed)"

    if worktree.branch:
        code, upstream = git(worktree.path, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
        if code == 0 and upstream:
            worktree.upstream = upstream
            code, counts = git(worktree.path, "rev-list", "--left-right", "--count", f"{worktree.branch}...{upstream}")
            if code == 0:
                ahead, behind = counts.split()
                worktree.ahead = int(ahead)
                worktree.behind = int(behind)

        code, merged = git(main_root, "branch", "--merged", "main")
        if code == 0:
            merged_names = {line.strip().lstrip("* ").strip() for line in merged.splitlines()}
            worktree.merged = worktree.branch in merged_names or worktree.branch == "main"

        branch_slug = slugify(worktree.branch)
        worktree.backlog_matches = [item for item in backlog_items if item.slug and item.slug in branch_slug]


def open_prs(root: Path) -> tuple[list[dict], str | None]:
    if not shutil.which("gh"):
        return [], "gh not found on PATH"
    code, output = gh(
        root,
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
    parser.add_argument("--repo", default=".", help="Repository or worktree path to audit.")
    args = parser.parse_args()

    try:
        root = repo_root(Path(args.repo).resolve())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    backlog_items = load_backlog(root)
    worktrees = parse_worktrees(root)
    for worktree in worktrees:
        fill_worktree_state(worktree, root, backlog_items)
    prs, pr_error = open_prs(root)

    print("# Finish Previous Work Report")
    print(f"Current date: {datetime.now().strftime('%Y-%m-%d %H%M')}")
    print(f"Anchor/root: {root}")

    section("Worktrees")
    for worktree in worktrees:
        print(f"- {worktree.path}")
        print(f"  branch: {worktree.branch or '(detached HEAD)'}")
        if worktree.upstream:
            print(f"  upstream: {worktree.upstream} (behind {worktree.behind}, ahead {worktree.ahead})")
        else:
            print("  upstream: (none)")
        print(f"  merged into main: {worktree.merged}")
        if worktree.backlog_matches:
            matches = ", ".join(f"{item.number}. {item.title}" for item in worktree.backlog_matches)
            print(f"  backlog: {matches}")
        if worktree.dirty:
            print("  changes:")
            for line in worktree.status.splitlines():
                print(f"    {line}")
        else:
            print("  changes: (none)")

    section("Open PRs")
    if pr_error:
        print(f"Could not check PRs: {pr_error}")
    elif prs:
        for pr in prs:
            draft = "draft" if pr.get("isDraft") else "ready"
            print(
                f"- #{pr.get('number')} {pr.get('title')} [{draft}] "
                f"{pr.get('headRefName')} -> {pr.get('baseRefName')} "
                f"mergeable={pr.get('mergeable')} {pr.get('url')}"
            )
    else:
        print("(none)")

    section("Recommendations")
    dirty = [worktree for worktree in worktrees if worktree.dirty]
    no_upstream = [worktree for worktree in worktrees if worktree.branch and worktree.branch != "main" and not worktree.upstream]
    ahead = [worktree for worktree in worktrees if worktree.ahead and worktree.ahead > 0]
    clean_merged = [
        worktree
        for worktree in worktrees
        if worktree.branch and worktree.branch != "main" and worktree.merged and not worktree.dirty
    ]

    if dirty:
        print("- Review local changes before switching context, syncing, or deleting worktrees.")
    if no_upstream:
        print("- Publish or explicitly archive branches without upstreams before cleanup.")
    if ahead:
        print("- Push or open PRs for branches ahead of upstream.")
    if prs:
        print("- Review open PRs; merge externally, then sync main and remove clean merged worktrees.")
    if clean_merged:
        names = ", ".join(worktree.branch for worktree in clean_merged)
        print(f"- Clean merged worktrees can be removed after confirmation: {names}.")
    if not any([dirty, no_upstream, ahead, prs, clean_merged]):
        print("- No leftover work detected. Ready to sync main and start new work.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
