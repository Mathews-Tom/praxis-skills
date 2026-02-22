"""Tests for scripts/generate_manifest.py."""
from __future__ import annotations

from pathlib import Path

import yaml

from scripts.generate_manifest import collect_skills, parse_frontmatter, write_manifest


class TestParseFrontmatter:
    """Tests for frontmatter extraction."""

    def test_extracts_all_fields(self) -> None:
        content = "---\nname: my-skill\ndescription: Does things.\nmetadata:\n  version: 1.2.3\n---\n# Body"
        meta = parse_frontmatter(content)
        assert meta["name"] == "my-skill"
        assert meta["metadata"]["version"] == "1.2.3"
        assert meta["description"] == "Does things."

    def test_raises_on_missing_frontmatter(self) -> None:
        import pytest

        with pytest.raises(ValueError, match="No valid YAML frontmatter"):
            parse_frontmatter("# No frontmatter")


class TestCollectSkills:
    """Tests for skill collection from SKILL.md files."""

    def test_collects_from_real_repo(self) -> None:
        """Verify collect_skills finds all 18 skills in the actual repo."""
        entries = collect_skills()
        assert len(entries) == 18

        names = {e["name"] for e in entries}
        assert "agent-builder" in names
        assert "tavily" in names

        for entry in entries:
            assert entry["version"] == "1.0.0"
            assert entry["path"].startswith("skills/")
            assert entry["description"]


class TestWriteManifest:
    """Tests for manifest file generation."""

    def test_writes_valid_yaml(self, tmp_path: Path) -> None:
        entries = [
            {
                "name": "test-skill",
                "version": "1.0.0",
                "description": "A test skill.",
                "path": "skills/test-skill",
            }
        ]

        # Temporarily override MANIFEST_PATH
        import scripts.generate_manifest as gm

        original = gm.MANIFEST_PATH
        gm.MANIFEST_PATH = tmp_path / "skills.yaml"

        try:
            write_manifest(entries)

            content = gm.MANIFEST_PATH.read_text()
            assert "Auto-generated" in content

            data = yaml.safe_load(content)
            assert len(data["skills"]) == 1
            assert data["skills"][0]["name"] == "test-skill"
            assert data["skills"][0]["version"] == "1.0.0"
        finally:
            gm.MANIFEST_PATH = original
