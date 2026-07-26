#!/usr/bin/env python3
"""Open a draft pull request for the current published branch."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
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


def remote_default_branch(root: Path) -> str:
    code, output = gh(root, "repo", "view", "--json", "defaultBranchRef")
    if code != 0:
        return "main"
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return "main"
    branch = data.get("defaultBranchRef", {}).get("name")
    return branch or "main"


def repo_full_name(root: Path) -> str | None:
    code, output = gh(root, "repo", "view", "--json", "nameWithOwner")
    if code != 0:
        return None
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return None
    return data.get("nameWithOwner")


def print_status(status: str) -> None:
    print(status if status.strip() else "(none)")


def body_text(args: argparse.Namespace) -> str:
    if args.body_file:
        return Path(args.body_file).read_text(encoding="utf-8")
    summary = args.summary or "Describe the changes in this branch."
    validation = args.validation or ["Not recorded."]
    risks = args.risk or ["No known risks."]
    validation_lines = "\n".join(f"- `{item}`" for item in validation)
    risk_lines = "\n".join(f"- {item}" for item in risks)
    return f"""## Summary

- {summary}

## Validation

{validation_lines}

## Risks

{risk_lines}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository or worktree path.")
    parser.add_argument("--title", help="Pull request title. Required with --apply.")
    parser.add_argument("--base", help="Base branch. Defaults to the repository default branch.")
    parser.add_argument("--body-file", help="Markdown file to use as the pull request body.")
    parser.add_argument("--summary", help="One summary bullet used when --body-file is omitted.")
    parser.add_argument("--validation", action="append", default=[], help="Validation result or command. Repeat as needed.")
    parser.add_argument("--risk", action="append", default=[], help="Known risk note. Repeat as needed.")
    parser.add_argument("--ready", action="store_true", help="Create a ready-for-review PR instead of a draft.")
    parser.add_argument("--apply", action="store_true", help="Create the pull request.")
    args = parser.parse_args()

    try:
        root = repo_root(Path(args.repo).resolve())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    branch = current_branch(root)
    status = status_short(root)
    tracked_upstream = upstream(root)
    default_base = args.base or remote_default_branch(root)
    full_name = repo_full_name(root) or "(unknown)"
    draft = not args.ready

    print("# Create PR Report")
    print(f"Current date: {datetime.now().strftime('%Y-%m-%d %H%M')}")
    print(f"Repository: {root}")
    print(f"GitHub repo: {full_name}")
    print(f"Current branch: {branch or '(detached HEAD)'}")
    print(f"Upstream: {tracked_upstream or '(none)'}")
    print(f"Base branch: {default_base}")
    print(f"Draft: {draft}")

    section("Local Changed Files")
    print_status(status)

    section("Readiness")
    if not branch:
        print("Stopped: detached HEAD. Check out a published feature branch first.")
        return 1
    if branch in {"main", "master", default_base}:
        print("Stopped: refusing to open a PR from the default branch.")
        return 1
    if status.strip():
        print("Stopped: worktree has local changes. Publish the branch before creating a PR.")
        return 1
    if not tracked_upstream:
        print("Stopped: no upstream configured. Push the branch before creating a PR.")
        return 1
    if args.apply and not args.title:
        print("Stopped: --title is required with --apply.")
        return 1

    section("Body Preview")
    body = body_text(args)
    print(body.rstrip())

    section("Action")
    if not args.apply:
        print("Dry run: no pull request was created.")
        return 0

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as handle:
        handle.write(body)
        body_path = Path(handle.name)

    command = ["pr", "create", "--base", default_base, "--head", branch, "--title", args.title or "", "--body-file", str(body_path)]
    if draft:
        command.append("--draft")

    code, output = gh(root, *command)
    try:
        body_path.unlink(missing_ok=True)
    except OSError:
        pass
    print(output)
    if code != 0:
        print("Stopped: gh pr create failed.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
