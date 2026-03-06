#!/usr/bin/env python3
"""Validate eval cases.yaml files across all skills."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

REQUIRED_CASE_FIELDS = {"id", "prompt", "rubric", "trigger_expected"}


def is_deprecated(skill_dir: Path) -> bool:
    """Check if a skill is deprecated by reading its SKILL.md frontmatter."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False
    try:
        text = skill_md.read_text(encoding="utf-8")
        if not text.startswith("---"):
            return False
        end = text.index("---", 3)
        frontmatter = yaml.safe_load(text[3:end])
        return (
            isinstance(frontmatter, dict)
            and frontmatter.get("metadata", {}).get("status") == "deprecated"
        )
    except (ValueError, yaml.YAMLError):
        return False


def validate_case(case: dict, skill_name: str, idx: int) -> list[str]:
    """Validate a single eval case and return errors."""
    errors: list[str] = []
    prefix = f"{skill_name} case #{idx}"

    missing = REQUIRED_CASE_FIELDS - set(case.keys())
    if missing:
        errors.append(f"{prefix}: missing required fields: {missing}")
        return errors

    if not isinstance(case["id"], str) or not case["id"]:
        errors.append(f"{prefix}: 'id' must be a non-empty string")

    if not isinstance(case["prompt"], str) or not case["prompt"].strip():
        errors.append(f"{prefix}: 'prompt' must be a non-empty string")

    if not isinstance(case["trigger_expected"], bool):
        errors.append(f"{prefix}: 'trigger_expected' must be a boolean")

    if not isinstance(case["rubric"], list) or len(case["rubric"]) == 0:
        errors.append(f"{prefix}: 'rubric' must be a non-empty list")

    return errors


def validate_skill_evals(skill_dir: Path) -> list[str]:
    """Validate evals/cases.yaml for a single skill."""
    cases_file = skill_dir / "evals" / "cases.yaml"
    if not cases_file.exists():
        return []

    skill_name = skill_dir.name
    deprecated = is_deprecated(skill_dir)
    errors: list[str] = []

    try:
        data = yaml.safe_load(cases_file.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return [f"{skill_name}: invalid YAML in cases.yaml: {e}"]

    if not isinstance(data, dict) or "cases" not in data:
        return [f"{skill_name}: cases.yaml must have a top-level 'cases' key"]

    cases = data["cases"]
    if not isinstance(cases, list) or len(cases) == 0:
        return [f"{skill_name}: 'cases' must be a non-empty list"]

    ids: set[str] = set()
    positive_count = 0
    negative_count = 0

    for i, case in enumerate(cases, 1):
        errors.extend(validate_case(case, skill_name, i))

        case_id = case.get("id", "")
        if case_id in ids:
            errors.append(f"{skill_name} case #{i}: duplicate id '{case_id}'")
        ids.add(case_id)

        if case.get("trigger_expected") is True:
            positive_count += 1
        elif case.get("trigger_expected") is False:
            negative_count += 1

    if deprecated:
        if positive_count > 0:
            errors.append(f"{skill_name}: deprecated skill must have 0 positive cases, found {positive_count}")
    else:
        if positive_count == 0:
            errors.append(f"{skill_name}: must have at least 1 positive case (trigger_expected: true)")

    if negative_count < 2:
        errors.append(f"{skill_name}: must have at least 2 negative cases (trigger_expected: false), found {negative_count}")

    return errors


def main() -> int:
    """Validate all eval cases across skills."""
    all_errors: list[str] = []
    validated = 0

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        cases_file = skill_dir / "evals" / "cases.yaml"
        if not cases_file.exists():
            continue

        errors = validate_skill_evals(skill_dir)
        all_errors.extend(errors)
        validated += 1

    if all_errors:
        print(f"FAILED: {len(all_errors)} error(s) in {validated} eval file(s):", file=sys.stderr)
        for error in all_errors:
            print(f"  {error}", file=sys.stderr)
        return 1

    print(f"Validated {validated} eval file(s) — all passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
