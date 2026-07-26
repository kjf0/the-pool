#!/usr/bin/env python3
"""Report project note and memory hygiene context."""

from __future__ import annotations

import argparse
import json
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


def changed_files(root: Path) -> list[str]:
    code, output = git(root, "status", "--short")
    if code != 0 or not output:
        return []
    return [line[3:] for line in output.splitlines() if len(line) > 3]


def load_backlog(root: Path) -> list[dict]:
    path = root / "public_html" / "backlog-data.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository or worktree path to inspect.")
    args = parser.parse_args()

    try:
        root = repo_root(Path(args.repo).resolve())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    changed = changed_files(root)
    backlog = load_backlog(root)
    note_files = sorted(str(path.relative_to(root)) for path in (root / "notes").glob("*.md"))

    print("# Project Memory Curator Report")
    print(f"Current date: {datetime.now().strftime('%Y-%m-%d %H%M')}")
    print(f"Repository: {root}")

    section("Changed Files")
    if changed:
        for file in changed:
            print(f"- {file}")
    else:
        print("(none)")

    section("Repo Notes")
    for file in note_files:
        print(f"- {file}")

    section("Backlog Source")
    if backlog:
        done = sum(1 for item in backlog if str(item.get("status", "")).lower() == "done")
        open_items = len(backlog) - done
        print(f"public_html\\backlog-data.json: {len(backlog)} items ({done} done, {open_items} open)")
    else:
        print("No structured backlog JSON found.")

    section("Recommended Memory Action")
    if any(file.startswith("notes/") or file.startswith("public_html/backlog-data.json") for file in changed):
        print("- Update repo notes or backlog JSON in this PR when the change should persist for the project.")
    else:
        print("- No repo note update appears necessary from the changed files alone.")
    print("- Add personal Codex memory update notes only when the user explicitly asks.")
    print("- Keep durable memory short, evidence-based, and focused on repeatable workflow lessons.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
