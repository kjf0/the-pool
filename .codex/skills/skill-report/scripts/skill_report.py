#!/usr/bin/env python3
"""List repo-owned Codex skills for the current project."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Skill:
    name: str
    description: str
    group: str
    path: Path


def run(cwd: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def git(repo: Path, *args: str) -> tuple[int, str]:
    result = run(repo, ["git", *args])
    return result.returncode, (result.stdout + result.stderr).rstrip()


def repo_root(repo: Path) -> Path:
    code, output = git(repo, "rev-parse", "--show-toplevel")
    if code != 0:
        raise RuntimeError(output or f"Not a git repository: {repo}")
    return Path(output).resolve()


def frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, flags=re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip('"')


def skill_group(name: str, description: str) -> str:
    known_groups = {
        "create-feature-worktree": "Git workflow",
        "finish-previous-work": "Git workflow",
        "start-coding-day": "Git workflow",
        "sync-feature-branch-with-main": "Git workflow",
        "sync-local-main": "Git workflow",
        "create-pr": "Publishing",
        "publish-branch-worktree": "Publishing",
        "modify-code-workflow": "Development",
        "project-memory-curator": "Project memory",
        "skill-report": "Reporting",
        "status-summary": "Reporting",
    }
    if name in known_groups:
        return known_groups[name]
    text = f"{name} {description}".lower()
    words = set(re.findall(r"[a-z0-9]+", text))
    if "github" in words or "pr" in words or "publish" in words or "publishing" in words:
        return "Publishing"
    if {"worktree", "branch", "sync", "git", "main"} & words:
        return "Git workflow"
    if {"memory", "notes", "backlog"} & words:
        return "Project memory"
    if {"report", "summary"} & words:
        return "Reporting"
    return "Workflow"


def load_skills(root: Path) -> list[Skill]:
    skills_path = root / ".codex" / "skills"
    skills: list[Skill] = []
    for skill_dir in sorted(path for path in skills_path.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        text = skill_file.read_text(encoding="utf-8")
        name = frontmatter_value(text, "name") or skill_dir.name
        description = frontmatter_value(text, "description")
        skills.append(Skill(name=name, description=description, group=skill_group(name, description), path=skill_dir))
    return skills


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository or worktree path to inspect.")
    args = parser.parse_args()

    try:
        root = repo_root(Path(args.repo).resolve())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    skills = load_skills(root)

    print("# Skill Report")
    print(f"Current date: {datetime.now().strftime('%Y-%m-%d %H%M')}")
    print(f"Repository: {root}")
    print(f"Skill source: {root / '.codex' / 'skills'}")
    print(f"Repo-owned skills: {len(skills)}")

    current_group = ""
    for skill in sorted(skills, key=lambda item: (item.group, item.name)):
        if skill.group != current_group:
            current_group = skill.group
            print(f"\n## {current_group}")
        print(f"- {skill.name}: {skill.description}")

    print("\n## Policy")
    print("- Prefer repo-owned skills under .codex\\skills for this project.")
    print("- Avoid personal duplicates unless there is a specific reason.")
    print("- See notes\\shared_skills_strategy.md for sharing policy.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
