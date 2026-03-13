#!/usr/bin/env python3
"""Sync shared template files into consuming skill directories."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "_templates"
SKILLS_DIR = REPO_ROOT / "skills"

TEMPLATE_CONSUMERS: dict[str, list[str]] = {
    "detection-patterns.md": ["humanize", "linkedin-post-style", "manuscript-review"],
    "project-detection.md": ["ship-workflow", "plan-review", "qa-systematic"],
}


def sync_template(template_name: str, consumers: list[str]) -> list[str]:
    """Sync a single template to all its consumers. Returns list of updated paths."""
    source = TEMPLATES_DIR / template_name
    if not source.exists():
        print(f"  skip: {template_name} (template not yet created)", file=sys.stderr)
        return []

    source_content = source.read_bytes()
    updated: list[str] = []

    for skill_name in consumers:
        target_dir = SKILLS_DIR / skill_name / "references"
        target = target_dir / template_name

        if target.exists() and target.read_bytes() == source_content:
            continue

        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        rel = target.relative_to(REPO_ROOT)
        updated.append(str(rel))
        print(f"  synced: {rel}")

    return updated


def main() -> int:
    """Sync all templates to their consumers."""
    all_updated: list[str] = []

    for template_name, consumers in TEMPLATE_CONSUMERS.items():
        updated = sync_template(template_name, consumers)
        all_updated.extend(updated)

    if all_updated:
        print(f"\n{len(all_updated)} file(s) updated — re-stage and commit")
        return 1

    print("All templates in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
