#!/usr/bin/env python3
"""Synchronize a feature branch with the current local main."""

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
    print(status if status.strip() else "(none)")


def main_worktree_path(repo: Path) -> Path:
    code, output = git(repo, "worktree", "list", "--porcelain")
    if code != 0:
        return repo
    for line in output.splitlines():
        if line.startswith("worktree "):
            return Path(line.removeprefix("worktree ")).resolve()
    return repo


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Feature worktree path to sync.")
    parser.add_argument("--apply", action="store_true", help="Fetch, fast-forward main, and merge main into the feature branch.")
    parser.add_argument("--no-fetch", action="store_true", help="Skip fetch before checking origin/main.")
    args = parser.parse_args()

    try:
        root = repo_root(Path(args.repo).resolve())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    branch = current_branch(root)
    status = status_short(root)
    main_path = main_worktree_path(root)

    print("# Sync Feature Branch With Main Report")
    print(f"Current date: {datetime.now().strftime('%Y-%m-%d %H%M')}")
    print(f"Feature worktree: {root}")
    print(f"Main anchor: {main_path}")
    print(f"Current branch: {branch or '(detached HEAD)'}")

    section("Local Changed Files")
    print_status(status)

    section("Readiness")
    if not branch:
        print("Stopped: detached HEAD. Check out a feature branch first.")
        return 1
    if branch in {"main", "master"}:
        print("Stopped: run this from a feature branch, not the main anchor.")
        return 1
    if status.strip():
        print("Stopped: feature worktree has local changes. Commit, stash by explicit request, or finish them first.")
        return 1
    if not ref_exists(root, "main"):
        print("Stopped: local main does not exist.")
        return 1
    if not ref_exists(root, "origin/main"):
        print("Stopped: origin/main does not exist.")
        return 1

    section("Fetch")
    if args.no_fetch:
        print("Skipped by --no-fetch.")
    else:
        if args.apply:
            code, output = git(root, "fetch", "origin", "--prune")
            print(output or "Fetched origin --prune.")
            if code != 0:
                print("Stopped: fetch failed.")
                return 1
        else:
            print("Dry run: fetch would run with --apply.")

    section("Main Comparison")
    try:
        main_ahead, main_behind = ahead_behind(root, "main", "origin/main")
    except RuntimeError as exc:
        print(f"Stopped: {exc}")
        return 1
    print(f"main compared with origin/main: behind {main_behind}, ahead {main_ahead}.")
    if main_ahead > 0:
        print("Stopped: local main has commits not on origin/main. Inspect before syncing.")
        return 1

    section("Feature Comparison")
    try:
        feature_ahead, feature_behind = ahead_behind(root, branch, "main")
    except RuntimeError as exc:
        print(f"Stopped: {exc}")
        return 1
    print(f"{branch} compared with main: behind {feature_behind}, ahead {feature_ahead}.")

    section("Action")
    if not args.apply:
        print("Dry run: no branches were changed.")
        return 0

    if main_behind:
        code, output = git(main_path, "merge", "--ff-only", "origin/main")
        print(output or "Fast-forwarded main from origin/main.")
        if code != 0:
            print("Stopped: fast-forwarding main failed.")
            return 1

    code, output = git(root, "merge", "--no-edit", "main")
    print(output or "Merged main into the feature branch.")
    if code != 0:
        print("Stopped: merge main into feature branch failed. Resolve conflicts, then run validation.")
        return 1

    print("Feature branch is synced with main. Run validation for the active work before publishing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
