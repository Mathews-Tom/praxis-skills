#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

import yaml


EXCLUDE_NAMES: set[str] = {
    "__pycache__",
    "node_modules",
    ".DS_Store",
    ".git",
    "evals",
}

EXCLUDE_SUFFIXES: set[str] = {".pyc"}


def parse_frontmatter(content: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        raise ValueError("No valid YAML frontmatter found in SKILL.md")
    return yaml.safe_load(match.group(1))


def validate_version(version: str) -> None:
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        raise ValueError(f"Invalid version '{version}' — must be semver (e.g. 1.0.0)")


def validate_frontmatter(skill_dir: Path) -> dict[str, str]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")

    content = skill_md.read_text(encoding="utf-8")
    meta = parse_frontmatter(content)

    missing = [field for field in ("name", "version", "description") if not meta.get(field)]
    if missing:
        raise ValueError(f"SKILL.md missing required fields: {', '.join(missing)}")

    validate_version(meta["version"])

    return meta


def is_excluded(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    for part in relative.parts:
        if part in EXCLUDE_NAMES:
            return True
    if path.suffix in EXCLUDE_SUFFIXES:
        return True
    return False


def collect_files(skill_dir: Path) -> tuple[list[Path], list[Path]]:
    included: list[Path] = []
    excluded: list[Path] = []

    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        if is_excluded(path, skill_dir):
            excluded.append(path)
        else:
            included.append(path)

    return included, excluded


def package_skill(skill_dir: Path, output_dir: Path) -> Path:
    meta = validate_frontmatter(skill_dir)
    skill_name: str = meta["name"]
    skill_version: str = meta["version"]
    archive_name = f"{skill_name}-{skill_version}.skill"
    output_path = output_dir / archive_name

    included, excluded = collect_files(skill_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in included:
            arcname = file_path.relative_to(skill_dir.parent)
            zf.write(file_path, arcname)
            print(f"  added: {arcname}")

    for file_path in excluded:
        rel = file_path.relative_to(skill_dir)
        print(f"  skipped: {rel}")

    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Package a skill directory into a .skill archive")
    parser.add_argument("skill_dir", type=Path, help="Path to the skill directory")
    parser.add_argument("--output-dir", type=Path, default=Path("dist"), help="Output directory for .skill file")
    args = parser.parse_args()

    skill_dir: Path = args.skill_dir.resolve()
    output_dir: Path = args.output_dir.resolve()

    if not skill_dir.is_dir():
        print(f"ERROR: {skill_dir} is not a directory", file=sys.stderr)
        return 1

    try:
        output_path = package_skill(skill_dir, output_dir)
        print(f"Packaged: {output_path}")
        return 0
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
