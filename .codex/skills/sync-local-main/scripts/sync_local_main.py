#!/usr/bin/env python3
"""Safely fast-forward local main from origin/main."""

from __future__ import annotations

import argparse
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


def print_status(status: str) -> None:
    if status.strip():
        print(status)
    else:
        print("(none)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository or worktree path to sync.")
    parser.add_argument("--apply", action="store_true", help="Fetch origin and fast-forward local main when safe.")
    parser.add_argument("--fetch", action="store_true", help="Fetch origin --prune before reporting.")
    args = parser.parse_args()

    try:
        root = repo_root(Path(args.repo).resolve())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    should_fetch = args.apply or args.fetch
    branch = current_branch(root)
    status = status_short(root)

    print("# Sync Local Main Report")
    print(f"Current date: {datetime.now().strftime('%Y-%m-%d %H%M')}")
    print(f"Repository: {root}")
    print(f"Current branch: {branch or '(detached HEAD)'}")

    section("Local Changed Files")
    print_status(status)

    section("Fetch")
    if should_fetch:
        code, output = git(root, "fetch", "origin", "--prune")
        print(output or "Fetched origin --prune.")
        if code != 0:
            print("Stopped before sync because fetch failed.")
            return 1
    else:
        print("Skipped. Re-run with --fetch to refresh remotes or --apply to fetch and fast-forward.")

    section("Main Comparison")
    if not ref_exists(root, "main"):
        print("Stopped: local main does not exist.")
        return 1
    if not ref_exists(root, "origin/main"):
        print("Stopped: origin/main does not exist.")
        return 1

    try:
        ahead, behind = ahead_behind(root, "main", "origin/main")
    except RuntimeError as exc:
        print(f"Stopped: {exc}")
        return 1

    print(f"main compared with origin/main: behind {behind}, ahead {ahead}.")

    section("Action")
    if not args.apply:
        if behind == 0 and ahead == 0:
            print("Dry run: local main is aligned with origin/main.")
        elif ahead == 0:
            print("Dry run: local main can be fast-forwarded.")
        else:
            print("Dry run: local main has local commits or diverged; inspect before syncing.")
        return 0

    if branch != "main":
        print("Stopped: current worktree is not on main. Run from the main anchor/worktree before applying.")
        return 1
    if status.strip():
        print("Stopped: current worktree has local changes. Finish or explicitly move them before syncing main.")
        return 1
    if ahead > 0:
        print("Stopped: local main has commits not on origin/main. Inspect before merging or publishing.")
        return 1
    if behind == 0:
        print("Local main is already aligned with origin/main.")
        return 0

    code, output = git(root, "merge", "--ff-only", "origin/main")
    print(output or "Fast-forwarded main from origin/main.")
    if code != 0:
        print("Stopped: fast-forward failed.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
