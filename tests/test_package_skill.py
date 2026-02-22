"""Tests for scripts/package_skill.py."""
from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from scripts.package_skill import (
    is_excluded,
    package_skill,
    parse_frontmatter,
    validate_frontmatter,
    validate_version,
)


class TestParseFrontmatter:
    """Tests for frontmatter parsing."""

    def test_valid_frontmatter(self) -> None:
        content = "---\nname: test-skill\nversion: 1.0.0\ndescription: A test.\n---\n\n# Body"
        result = parse_frontmatter(content)
        assert result["name"] == "test-skill"
        assert result["version"] == "1.0.0"
        assert result["description"] == "A test."

    def test_multiline_description(self) -> None:
        content = "---\nname: test\nversion: 1.0.0\ndescription: >\n  Long description\n  across lines.\n---\n"
        result = parse_frontmatter(content)
        assert "Long description" in result["description"]

    def test_no_frontmatter(self) -> None:
        with pytest.raises(ValueError, match="No valid YAML frontmatter"):
            parse_frontmatter("# Just a heading\n\nNo frontmatter here.")


class TestValidateVersion:
    """Tests for semver validation."""

    def test_valid_versions(self) -> None:
        for v in ("0.0.0", "1.0.0", "1.2.3", "10.20.30"):
            validate_version(v)

    def test_invalid_versions(self) -> None:
        for v in ("1.0", "1", "v1.0.0", "1.0.0-beta", "abc", "1.0.0.0"):
            with pytest.raises(ValueError, match="Invalid version"):
                validate_version(v)


class TestValidateFrontmatter:
    """Tests for full frontmatter validation."""

    def test_missing_version(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: A test.\n---\n"
        )
        with pytest.raises(ValueError, match="missing required fields.*version"):
            validate_frontmatter(skill_dir)

    def test_invalid_version_format(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\nversion: v1.0\ndescription: A test.\n---\n"
        )
        with pytest.raises(ValueError, match="Invalid version"):
            validate_frontmatter(skill_dir)

    def test_valid_skill(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\nversion: 1.0.0\ndescription: A test.\n---\n"
        )
        meta = validate_frontmatter(skill_dir)
        assert meta["name"] == "test-skill"
        assert meta["version"] == "1.0.0"

    def test_missing_skill_md(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        with pytest.raises(FileNotFoundError):
            validate_frontmatter(skill_dir)


class TestIsExcluded:
    """Tests for file exclusion logic."""

    def test_pycache_excluded(self, tmp_path: Path) -> None:
        path = tmp_path / "__pycache__" / "module.pyc"
        assert is_excluded(path, tmp_path) is True

    def test_ds_store_excluded(self, tmp_path: Path) -> None:
        path = tmp_path / ".DS_Store"
        assert is_excluded(path, tmp_path) is True

    def test_pyc_excluded(self, tmp_path: Path) -> None:
        path = tmp_path / "module.pyc"
        assert is_excluded(path, tmp_path) is True

    def test_normal_file_included(self, tmp_path: Path) -> None:
        path = tmp_path / "SKILL.md"
        assert is_excluded(path, tmp_path) is False


class TestPackageSkill:
    """Tests for skill packaging."""

    def test_versioned_archive_name(self, tmp_path: Path) -> None:
        """Verify archive uses {name}-{version}.skill naming."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\nversion: 2.1.0\ndescription: A test.\n---\n# Content\n"
        )

        output_dir = tmp_path / "dist"
        result = package_skill(skill_dir, output_dir)

        assert result.name == "test-skill-2.1.0.skill"
        assert result.exists()
        assert zipfile.is_zipfile(result)

    def test_excludes_pycache(self, tmp_path: Path) -> None:
        """Verify __pycache__ is excluded from archive."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\nversion: 1.0.0\ndescription: A test.\n---\n"
        )
        pycache = skill_dir / "__pycache__"
        pycache.mkdir()
        (pycache / "cached.pyc").write_text("bytecode")

        output_dir = tmp_path / "dist"
        result = package_skill(skill_dir, output_dir)

        with zipfile.ZipFile(result) as zf:
            names = zf.namelist()
            assert not any("__pycache__" in n for n in names)
