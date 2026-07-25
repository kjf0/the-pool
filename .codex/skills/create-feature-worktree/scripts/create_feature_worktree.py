#!/usr/bin/env python3
"""Create a feature branch and trusted git worktree from main."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run(cwd: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def git(repo: Path, *args: str) -> tuple[int, str]:
    result = run(repo, ["git", *args])
    return result.returncode, (result.stdout + result.stderr).rstrip()


def section(title: str) -> None:
    print(f"\n## {title}")


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", text.strip().lower()).strip("-")
    return slug or "backlog-item"


def repo_root(repo: Path) -> Path:
    code, output = git(repo, "rev-parse", "--show-toplevel")
    if code != 0:
        raise RuntimeError(output or f"Not a git repository: {repo}")
    return Path(output).resolve()


def main_worktree_path(repo: Path) -> Path:
    code, output = git(repo, "worktree", "list", "--porcelain")
    if code != 0:
        return repo
    for line in output.splitlines():
        if line.startswith("worktree "):
            return Path(line.removeprefix("worktree ")).resolve()
    return repo


def remote_project_name(repo: Path) -> str | None:
    code, output = git(repo, "remote", "get-url", "origin")
    if code != 0 or not output:
        return None
    name = output.rstrip("/").split("/")[-1]
    if name.endswith(".git"):
        name = name[:-4]
    return slugify(name) if name else None


def default_worktrees_path(repo: Path) -> Path:
    main_path = main_worktree_path(repo)
    project_name = remote_project_name(repo) or slugify(main_path.name)
    return main_path.parent / "worktrees" / project_name


def current_branch(root: Path) -> str:
    code, output = git(root, "branch", "--show-current")
    if code != 0:
        return ""
    return output.strip()


def status_short(root: Path) -> str:
    code, output = git(root, "status", "--short")
    if code != 0:
        return output or "(status failed)"
    return output


def ref_exists(root: Path, ref: str) -> bool:
    code, _ = git(root, "rev-parse", "--verify", "--quiet", ref)
    return code == 0


def ahead_behind(root: Path, left: str, right: str) -> tuple[int, int]:
    code, output = git(root, "rev-list", "--left-right", "--count", f"{left}...{right}")
    if code != 0:
        raise RuntimeError(output or f"Could not compare {left} and {right}")
    ahead, behind = output.split()
    return int(ahead), int(behind)


def existing_worktree_paths(root: Path) -> set[Path]:
    code, output = git(root, "worktree", "list", "--porcelain")
    if code != 0:
        return set()
    paths = set()
    for line in output.splitlines():
        if line.startswith("worktree "):
            paths.add(Path(line.removeprefix("worktree ")).resolve())
    return paths


def safe_directory_values(root: Path) -> set[str]:
    code, output = git(root, "config", "--global", "--get-all", "safe.directory")
    if code != 0 or not output:
        return set()
    return {line.strip() for line in output.splitlines() if line.strip()}


def git_safe_path(path: Path) -> str:
    return path.resolve().as_posix()


def print_status(status: str) -> None:
    if status.strip():
        print(status)
    else:
        print("(none)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Main repository path.")
    parser.add_argument("--backlog-item", required=True, help="Backlog item title or short description.")
    parser.add_argument("--apply", action="store_true", help="Create the branch/worktree and trust its exact path.")
    parser.add_argument("--branch", help="Full branch name to create. Defaults to codex/<generated-name>.")
    parser.add_argument("--worktree-name", help="Worktree folder name. Defaults to the generated timestamped slug.")
    parser.add_argument("--worktrees-path", help="Parent folder for project worktrees.")
    args = parser.parse_args()

    try:
        root = repo_root(Path(args.repo).resolve())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    now = datetime.now()
    generated_name = f"{now.strftime('%Y-%m-%d_%H%M')}-{slugify(args.backlog_item)}"
    worktree_name = args.worktree_name or generated_name
    branch = args.branch or f"codex/{worktree_name}"
    parent = Path(args.worktrees_path).resolve() if args.worktrees_path else default_worktrees_path(root)
    worktree_path = (parent / worktree_name).resolve()
    safe_path = git_safe_path(worktree_path)
    status = status_short(root)
    current = current_branch(root)

    print("# Create Feature Worktree Report")
    print(f"Current date: {now.strftime('%Y-%m-%d %H%M')}")
    print(f"Repository: {root}")
    print(f"Current branch: {current or '(detached HEAD)'}")
    print(f"Generated name: {generated_name}")
    print(f"Branch: {branch}")
    print(f"Worktree path: {worktree_path}")
    print(f"Safe directory path: {safe_path}")

    section("Local Changed Files")
    print_status(status)

    section("Main Readiness")
    if current != "main":
        print("Stopped: run from the main anchor/worktree before creating a new feature worktree.")
        return 1
    if status.strip():
        print("Stopped: main worktree has local changes.")
        return 1
    if not ref_exists(root, "main"):
        print("Stopped: local main does not exist.")
        return 1
    if not ref_exists(root, "origin/main"):
        print("Stopped: origin/main does not exist. Sync local main first.")
        return 1
    try:
        ahead, behind = ahead_behind(root, "main", "origin/main")
    except RuntimeError as exc:
        print(f"Stopped: {exc}")
        return 1
    print(f"main compared with origin/main: behind {behind}, ahead {ahead}.")
    if ahead or behind:
        print("Stopped: sync local main before creating a new feature worktree.")
        return 1

    section("Collision Checks")
    if ref_exists(root, branch):
        print(f"Stopped: branch already exists: {branch}")
        return 1
    existing_paths = existing_worktree_paths(root)
    if worktree_path in existing_paths or worktree_path.exists():
        print(f"Stopped: worktree path already exists: {worktree_path}")
        return 1
    print("No branch or worktree path collision detected.")

    section("Action")
    if not args.apply:
        print("Dry run: no branch, worktree, or safe.directory entry was created.")
        return 0

    parent.mkdir(parents=True, exist_ok=True)
    code, output = git(root, "worktree", "add", "-b", branch, str(worktree_path), "main")
    print(output or "Created worktree.")
    if code != 0:
        print("Stopped: git worktree add failed.")
        return 1

    safe_values = safe_directory_values(root)
    if safe_path in safe_values:
        print(f"safe.directory already trusted: {safe_path}")
    else:
        code, output = git(root, "config", "--global", "--add", "safe.directory", safe_path)
        if output:
            print(output)
        if code != 0:
            print("Stopped: worktree was created, but safe.directory update failed.")
            return 1
        print(f"Added safe.directory: {safe_path}")

    section("Next Step")
    print(f"cd {worktree_path}")
    print("Run status checks from the new worktree before editing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
