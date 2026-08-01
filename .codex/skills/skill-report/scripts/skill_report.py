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
    short_description: str
    short_description_source: str
    group: str
    path: Path
    overview: list[str]
    workflow: list[str]
    safety_rules: list[str]


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


def yaml_value(text: str, key: str) -> str:
    match = re.search(rf"^\s*{re.escape(key)}:\s*(.+)$", text, flags=re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip('"')


def first_sentence(text: str) -> str:
    sentence = re.split(r"(?<=[.!?])\s+", text.strip(), maxsplit=1)[0]
    return sentence.rstrip(".")


def section_text(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$([\s\S]*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE,
    )
    return match.group(1).strip() if match else ""


def pseudocode_lines(section: str) -> list[str]:
    lines: list[str] = []
    in_code = False
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line:
            continue
        line = re.sub(r"^\d+\.\s+", "", line)
        line = re.sub(r"^[-*]\s+", "", line)
        line = line.strip()
        if line:
            lines.append(line)
    return lines


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
        agent_file = skill_dir / "agents" / "openai.yaml"
        agent_text = agent_file.read_text(encoding="utf-8") if agent_file.exists() else ""
        agent_short_description = yaml_value(agent_text, "short_description")
        short_description = agent_short_description or first_sentence(description)
        short_description_source = "agents/openai.yaml" if agent_short_description else "SKILL.md description"
        skills.append(
            Skill(
                name=name,
                description=description,
                short_description=short_description,
                short_description_source=short_description_source,
                group=skill_group(name, description),
                path=skill_dir,
                overview=pseudocode_lines(section_text(text, "Overview")),
                workflow=pseudocode_lines(section_text(text, "Workflow")),
                safety_rules=pseudocode_lines(section_text(text, "Safety Rules")),
            )
        )
    return skills


def print_verbose_skill(root: Path, skill: Skill) -> None:
    rel_path = skill.path.relative_to(root)
    print(f"  source: {rel_path}")
    print(f"  description: {skill.description}")
    print("  decisions:")
    print(f"    - group: {skill.group}")
    print(f"    - short_description: {skill.short_description_source}")
    print("    - verbose_detail: SKILL.md Overview, Workflow, and Safety Rules sections")
    if skill.overview:
        print("  overview:")
        for line in skill.overview:
            print(f"    - {line}")
    if skill.workflow:
        print("  workflow:")
        for line in skill.workflow:
            print(f"    - {line}")
    if skill.safety_rules:
        print("  safety:")
        for line in skill.safety_rules:
            print(f"    - {line}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository or worktree path to inspect.")
    parser.add_argument("--verbose", action="store_true", help="Include pseudocode-style workflow details for each skill.")
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
        print(f"- {skill.name} - {skill.short_description}")
        if args.verbose:
            print_verbose_skill(root, skill)

    print("\n## Policy")
    print("- Prefer repo-owned skills under .codex\\skills for this project.")
    print("- Avoid personal duplicates unless there is a specific reason.")
    print("- See notes\\shared_skills_strategy.md for sharing policy.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
