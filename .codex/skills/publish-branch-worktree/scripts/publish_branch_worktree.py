#!/usr/bin/env python3
"""Prepare, commit, and push the current feature branch."""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run(cwd: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def run_shell(cwd: Path, command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


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


def upstream(root: Path) -> str | None:
    code, output = git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if code != 0:
        return None
    return output.strip()


def print_status(status: str) -> None:
    print(status if status.strip() else "(none)")


def quote_files(files: list[str]) -> str:
    return " ".join(shlex.quote(file) for file in files)


def run_checks(root: Path, checks: list[str]) -> bool:
    ok = True
    for command in checks:
        result = run_shell(root, command)
        print(f"$ {command}")
        output = (result.stdout + result.stderr).rstrip()
        print(output or "(no output)")
        if result.returncode != 0:
            print(f"Check failed with exit code {result.returncode}.")
            ok = False
            break
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository or worktree path to publish.")
    parser.add_argument("--message", help="Commit message. Required with --apply.")
    parser.add_argument("--file", action="append", default=[], help="Intentional file path to stage. Repeat as needed.")
    parser.add_argument("--all-changes", action="store_true", help="Stage every local change after scope review.")
    parser.add_argument("--check", action="append", default=[], help="Validation command to run before commit. Repeat as needed.")
    parser.add_argument("--apply", action="store_true", help="Run checks, stage, commit, and push.")
    args = parser.parse_args()

    try:
        root = repo_root(Path(args.repo).resolve())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    branch = current_branch(root)
    status = status_short(root)
    tracked_upstream = upstream(root)
    checks = args.check or ["git diff --check"]

    print("# Publish Branch Worktree Report")
    print(f"Current date: {datetime.now().strftime('%Y-%m-%d %H%M')}")
    print(f"Repository: {root}")
    print(f"Current branch: {branch or '(detached HEAD)'}")
    print(f"Upstream: {tracked_upstream or '(none)'}")

    section("Local Changed Files")
    print_status(status)

    section("Scope")
    if args.all_changes:
        print("Stage plan: all local changes.")
    elif args.file:
        print("Stage plan: explicit files.")
        for file in args.file:
            print(f"- {file}")
    else:
        print("Stage plan: none supplied.")

    section("Validation Plan")
    for command in checks:
        print(f"- {command}")

    section("Readiness")
    if not branch:
        print("Stopped: detached HEAD. Check out a feature branch before publishing.")
        return 1
    if branch in {"main", "master"}:
        print("Stopped: refusing to publish directly from the default branch.")
        return 1
    if not status.strip():
        print("Stopped: no local changes to commit.")
        return 1
    if args.all_changes and args.file:
        print("Stopped: use either --all-changes or --file, not both.")
        return 1
    if not args.all_changes and not args.file:
        print("Stopped: provide --file for intentional paths or --all-changes after scope review.")
        return 1
    if args.apply and not args.message:
        print("Stopped: --message is required with --apply.")
        return 1

    section("Action")
    if not args.apply:
        print("Dry run: no files were staged, committed, or pushed.")
        return 0

    if not run_checks(root, checks):
        print("Stopped: validation failed.")
        return 1

    if args.all_changes:
        code, output = git(root, "add", "-A")
    else:
        code, output = git(root, "add", "--", *args.file)
    print(output or "Staged intended changes.")
    if code != 0:
        print("Stopped: git add failed.")
        return 1

    code, staged = git(root, "diff", "--cached", "--stat")
    section("Staged Diff")
    print(staged or "(none)")
    if code != 0 or not staged.strip():
        print("Stopped: no staged changes.")
        return 1

    code, output = git(root, "commit", "-m", args.message or "")
    print(output)
    if code != 0:
        print("Stopped: git commit failed.")
        return 1

    if tracked_upstream:
        code, output = git(root, "push")
    else:
        code, output = git(root, "push", "-u", "origin", branch)
    print(output)
    if code != 0:
        print("Stopped: git push failed.")
        return 1

    print("Published branch successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
