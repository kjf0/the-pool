#!/usr/bin/env python3
"""Report repository readiness at the start of a coding session."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


TOOLS = ["git", "node", "npm", "pnpm", "gh"]


def run(repo: Path, args: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=repo,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git(repo: Path, *args: str) -> tuple[int, str]:
    result = run(repo, ["git", *args])
    output = (result.stdout + result.stderr).rstrip()
    return result.returncode, output


def section(title: str) -> None:
    print(f"\n## {title}")


def print_command(label: str, code: int, output: str) -> None:
    print(f"{label}: {'OK' if code == 0 else 'FAILED'}")
    if output:
        print(output)


def current_branch(repo: Path) -> str | None:
    code, output = git(repo, "branch", "--show-current")
    return output if code == 0 and output else None


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", text.strip().lower()).strip("-")
    return slug or "backlog-item"


def ahead_behind(repo: Path, branch: str) -> str:
    code, upstream = git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if code != 0:
        return "No upstream configured for current branch."
    code, counts = git(repo, "rev-list", "--left-right", "--count", f"{branch}...{upstream}")
    if code != 0:
        return f"Could not compare {branch} with {upstream}."
    ahead, behind = counts.split()
    return f"Compared with {upstream}: behind {behind}, ahead {ahead}."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository path to inspect.")
    parser.add_argument("--fetch", action="store_true", help="Run git fetch --prune before reporting.")
    parser.add_argument("--backlog-item", help="Backlog item description used to suggest branch/worktree names.")
    parser.add_argument("--worktrees-path", help="Directory where sibling worktrees should be created.")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.exists():
        print(f"Repository path does not exist: {repo}", file=sys.stderr)
        return 2

    code, output = git(repo, "rev-parse", "--show-toplevel")
    if code != 0:
        print(f"Not a git repository: {repo}", file=sys.stderr)
        return 2
    root = Path(output).resolve()
    anchor = root.parent
    worktrees_path = Path(args.worktrees_path).resolve() if args.worktrees_path else anchor
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H%M")
    path_safe_timestamp = now.strftime("%Y-%m-%d_%H%M")
    branch = current_branch(root)

    print("# Start Coding Day Report")
    print(f"Current date: {timestamp}")
    print(f"Project folder path: {root}")
    print(f"Anchor path: {anchor}")
    print(f"Worktrees path: {worktrees_path}")
    print(f"Current branch: {branch or '(detached HEAD)'}")
    if args.backlog_item:
        slug = slugify(args.backlog_item)
        print(f"Display label: {timestamp}-{slug}")
        print(f"Suggested branch/worktree name: {path_safe_timestamp}-{slug}")

    section("Local Changed Files")
    code, output = git(root, "status", "--short")
    print_command("git status --short", code, output or "(none)")

    if args.fetch:
        section("Fetch")
        code, output = git(root, "fetch", "--prune")
        print_command("git fetch --prune", code, output)

    section("Branch")
    code, output = git(root, "status", "--short", "--branch")
    print_command("git status --short --branch", code, output)
    if branch:
        print(ahead_behind(root, branch))

    section("Remotes")
    code, output = git(root, "remote", "-v")
    print_command("git remote -v", code, output)

    section("Worktrees")
    code, output = git(root, "worktree", "list", "--porcelain")
    print_command("git worktree list --porcelain", code, output)

    section("Main Comparison")
    code, output = git(root, "show-ref", "--verify", "--quiet", "refs/heads/main")
    has_main = code == 0
    code, output = git(root, "show-ref", "--verify", "--quiet", "refs/remotes/origin/main")
    has_origin_main = code == 0
    if has_main and has_origin_main:
        code, counts = git(root, "rev-list", "--left-right", "--count", "main...origin/main")
        if code == 0:
            ahead, behind = counts.split()
            print(f"main compared with origin/main: behind {behind}, ahead {ahead}.")
            if ahead == "0" and behind != "0":
                print("Local main can likely fast-forward if the worktree is clean and main is checked out.")
            elif ahead != "0" and behind != "0":
                print("Local main and origin/main have diverged; stop for a decision.")
            elif ahead != "0":
                print("Local main has commits not on origin/main; inspect before syncing.")
            else:
                print("Local main is aligned with origin/main.")
        else:
            print(f"Could not compare main and origin/main: {counts}")
    else:
        print(f"main exists locally: {has_main}")
        print(f"origin/main exists locally: {has_origin_main}")

    section("Tool Visibility")
    for tool in TOOLS:
        path = shutil.which(tool)
        print(f"{tool}: {path or 'not found on PATH'}")

    gh_path = Path("C:/Program Files/GitHub CLI/gh.exe")
    if not shutil.which("gh") and gh_path.exists():
        print(f"gh direct path exists: {gh_path}")

    section("Suggested Next Step")
    code, porcelain = git(root, "status", "--porcelain")
    dirty = bool(porcelain.strip())
    if dirty:
        print("Worktree has local changes. Review them before syncing, branching, or coding.")
    elif branch == "main":
        print("Worktree is clean on main. Fetch and fast-forward if needed, then begin work.")
    elif branch:
        print("Worktree is clean on a feature branch. Decide whether to continue it or create new work.")
    else:
        print("Detached HEAD. Decide which branch or worktree should become today's starting point.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
