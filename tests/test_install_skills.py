"""Tests for scripts/install_skills.py."""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.install_skills import (
    InstallAction,
    SkillInfo,
    build_install_plans,
    copy_skill,
    get_installed_version,
    is_newer,
    parse_selection,
    parse_version,
    should_exclude,
)


class TestParseVersion:
    """Tests for semver parsing."""

    def test_valid_version(self) -> None:
        assert parse_version("1.2.3") == (1, 2, 3)

    def test_zero_version(self) -> None:
        assert parse_version("0.0.0") == (0, 0, 0)

    def test_large_numbers(self) -> None:
        assert parse_version("10.20.30") == (10, 20, 30)

    def test_invalid_format(self) -> None:
        with pytest.raises(ValueError):
            parse_version("1.0")


class TestIsNewer:
    """Tests for version comparison."""

    def test_newer_major(self) -> None:
        assert is_newer("2.0.0", "1.0.0") is True

    def test_newer_minor(self) -> None:
        assert is_newer("1.1.0", "1.0.0") is True

    def test_newer_patch(self) -> None:
        assert is_newer("1.0.1", "1.0.0") is True

    def test_same_version(self) -> None:
        assert is_newer("1.0.0", "1.0.0") is False

    def test_older_version(self) -> None:
        assert is_newer("1.0.0", "2.0.0") is False


class TestParseSelection:
    """Tests for user input parsing."""

    def test_single_number(self) -> None:
        assert parse_selection("3", 10) == [2]

    def test_comma_separated(self) -> None:
        assert parse_selection("1,3,5", 10) == [0, 2, 4]

    def test_range(self) -> None:
        assert parse_selection("2-5", 10) == [1, 2, 3, 4]

    def test_mixed(self) -> None:
        assert parse_selection("1,3-5,8", 10) == [0, 2, 3, 4, 7]

    def test_all(self) -> None:
        assert parse_selection("all", 5) == [0, 1, 2, 3, 4]

    def test_quit(self) -> None:
        assert parse_selection("q", 10) == []

    def test_out_of_bounds(self) -> None:
        with pytest.raises(ValueError, match="out of bounds"):
            parse_selection("11", 10)

    def test_invalid_range(self) -> None:
        with pytest.raises(ValueError, match="out of bounds"):
            parse_selection("0-5", 10)

    def test_deduplication(self) -> None:
        assert parse_selection("1,1,1", 10) == [0]


class TestShouldExclude:
    """Tests for file exclusion during copy."""

    def test_pycache_excluded(self, tmp_path: Path) -> None:
        path = tmp_path / "__pycache__" / "mod.pyc"
        assert should_exclude(path, tmp_path) is True

    def test_ds_store_excluded(self, tmp_path: Path) -> None:
        path = tmp_path / ".DS_Store"
        assert should_exclude(path, tmp_path) is True

    def test_normal_file_included(self, tmp_path: Path) -> None:
        path = tmp_path / "SKILL.md"
        assert should_exclude(path, tmp_path) is False

    def test_evals_excluded(self, tmp_path: Path) -> None:
        path = tmp_path / "evals" / "test.json"
        assert should_exclude(path, tmp_path) is True


class TestGetInstalledVersion:
    """Tests for detecting installed skill versions."""

    def test_not_installed(self, tmp_path: Path) -> None:
        assert get_installed_version(tmp_path, "missing-skill") is None

    def test_installed_with_version(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\nversion: 1.2.3\ndescription: test\n---\n"
        )
        assert get_installed_version(tmp_path, "test-skill") == "1.2.3"

    def test_installed_without_version(self, tmp_path: Path) -> None:
        """Missing version field treated as 0.0.0."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: test\n---\n"
        )
        assert get_installed_version(tmp_path, "test-skill") == "0.0.0"

    def test_installed_with_bad_frontmatter(self, tmp_path: Path) -> None:
        """Invalid frontmatter treated as 0.0.0."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# No frontmatter\nJust content.")
        assert get_installed_version(tmp_path, "test-skill") == "0.0.0"


class TestBuildInstallPlans:
    """Tests for install plan generation."""

    def _make_skill(self, name: str, version: str, tmp_path: Path) -> SkillInfo:
        source = tmp_path / "repo" / name
        source.mkdir(parents=True, exist_ok=True)
        return SkillInfo(name=name, version=version, description="", source_path=source)

    def test_new_install(self, tmp_path: Path) -> None:
        install_dir = tmp_path / "install"
        install_dir.mkdir()
        skills = [self._make_skill("new-skill", "1.0.0", tmp_path)]
        plans = build_install_plans(skills, install_dir)
        assert len(plans) == 1
        assert plans[0].action == InstallAction.INSTALL
        assert plans[0].installed_version is None

    def test_upgrade(self, tmp_path: Path) -> None:
        install_dir = tmp_path / "install"
        skill_dir = install_dir / "old-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "---\nname: old-skill\nversion: 0.9.0\ndescription: test\n---\n"
        )
        skills = [self._make_skill("old-skill", "1.0.0", tmp_path)]
        plans = build_install_plans(skills, install_dir)
        assert plans[0].action == InstallAction.UPGRADE
        assert plans[0].installed_version == "0.9.0"

    def test_skip_same_version(self, tmp_path: Path) -> None:
        install_dir = tmp_path / "install"
        skill_dir = install_dir / "current-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "---\nname: current-skill\nversion: 1.0.0\ndescription: test\n---\n"
        )
        skills = [self._make_skill("current-skill", "1.0.0", tmp_path)]
        plans = build_install_plans(skills, install_dir)
        assert plans[0].action == InstallAction.SKIP

    def test_skip_symlink(self, tmp_path: Path) -> None:
        """Symlinked skills are skipped entirely."""
        install_dir = tmp_path / "install"
        install_dir.mkdir()
        (install_dir / "linked-skill").symlink_to(tmp_path)
        skills = [self._make_skill("linked-skill", "1.0.0", tmp_path)]
        plans = build_install_plans(skills, install_dir)
        assert len(plans) == 0


class TestCopySkill:
    """Tests for skill copying."""

    def test_copies_files(self, tmp_path: Path) -> None:
        source = tmp_path / "source"
        source.mkdir()
        (source / "SKILL.md").write_text("---\nname: test\nversion: 1.0.0\ndescription: t\n---\n")
        (source / "refs").mkdir()
        (source / "refs" / "data.txt").write_text("data")

        target = tmp_path / "target"
        count = copy_skill(source, target)

        assert count == 2
        assert (target / "SKILL.md").exists()
        assert (target / "refs" / "data.txt").exists()

    def test_excludes_pycache(self, tmp_path: Path) -> None:
        source = tmp_path / "source"
        source.mkdir()
        (source / "SKILL.md").write_text("---\nname: test\nversion: 1.0.0\ndescription: t\n---\n")
        (source / "__pycache__").mkdir()
        (source / "__pycache__" / "mod.pyc").write_text("bytecode")

        target = tmp_path / "target"
        count = copy_skill(source, target)

        assert count == 1
        assert not (target / "__pycache__").exists()

    def test_overwrites_existing(self, tmp_path: Path) -> None:
        """Upgrade scenario: existing target is removed first."""
        source = tmp_path / "source"
        source.mkdir()
        (source / "SKILL.md").write_text("---\nname: test\nversion: 2.0.0\ndescription: t\n---\n")

        target = tmp_path / "target"
        target.mkdir()
        (target / "old_file.txt").write_text("old")

        copy_skill(source, target)

        assert not (target / "old_file.txt").exists()
        assert (target / "SKILL.md").exists()
