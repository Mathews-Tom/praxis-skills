"""Tests for scripts/sync_templates.py."""
from __future__ import annotations

from pathlib import Path

from scripts.sync_templates import TEMPLATE_CONSUMERS, sync_template


class TestSyncTemplate:
    """Tests for template synchronization."""

    def test_copies_when_target_missing(self, tmp_path: Path, monkeypatch: object) -> None:
        import scripts.sync_templates as st

        templates_dir = tmp_path / "_templates"
        templates_dir.mkdir()
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        (skills_dir / "skill-a").mkdir()

        source = templates_dir / "test.md"
        source.write_text("template content")

        monkeypatch.setattr(st, "TEMPLATES_DIR", templates_dir)  # type: ignore[attr-defined]
        monkeypatch.setattr(st, "SKILLS_DIR", skills_dir)  # type: ignore[attr-defined]
        monkeypatch.setattr(st, "REPO_ROOT", tmp_path)  # type: ignore[attr-defined]

        updated = sync_template("test.md", ["skill-a"])

        target = skills_dir / "skill-a" / "references" / "test.md"
        assert target.exists()
        assert target.read_text() == "template content"
        assert len(updated) == 1

    def test_updates_when_target_differs(self, tmp_path: Path, monkeypatch: object) -> None:
        import scripts.sync_templates as st

        templates_dir = tmp_path / "_templates"
        templates_dir.mkdir()
        skills_dir = tmp_path / "skills"
        (skills_dir / "skill-a" / "references").mkdir(parents=True)

        source = templates_dir / "test.md"
        source.write_text("updated content")

        target = skills_dir / "skill-a" / "references" / "test.md"
        target.write_text("old content")

        monkeypatch.setattr(st, "TEMPLATES_DIR", templates_dir)  # type: ignore[attr-defined]
        monkeypatch.setattr(st, "SKILLS_DIR", skills_dir)  # type: ignore[attr-defined]
        monkeypatch.setattr(st, "REPO_ROOT", tmp_path)  # type: ignore[attr-defined]

        updated = sync_template("test.md", ["skill-a"])

        assert target.read_text() == "updated content"
        assert len(updated) == 1

    def test_noop_when_in_sync(self, tmp_path: Path, monkeypatch: object) -> None:
        import scripts.sync_templates as st

        templates_dir = tmp_path / "_templates"
        templates_dir.mkdir()
        skills_dir = tmp_path / "skills"
        (skills_dir / "skill-a" / "references").mkdir(parents=True)

        source = templates_dir / "test.md"
        source.write_text("same content")

        target = skills_dir / "skill-a" / "references" / "test.md"
        target.write_text("same content")

        monkeypatch.setattr(st, "TEMPLATES_DIR", templates_dir)  # type: ignore[attr-defined]
        monkeypatch.setattr(st, "SKILLS_DIR", skills_dir)  # type: ignore[attr-defined]
        monkeypatch.setattr(st, "REPO_ROOT", tmp_path)  # type: ignore[attr-defined]

        updated = sync_template("test.md", ["skill-a"])

        assert len(updated) == 0

    def test_creates_references_dir(self, tmp_path: Path, monkeypatch: object) -> None:
        import scripts.sync_templates as st

        templates_dir = tmp_path / "_templates"
        templates_dir.mkdir()
        skills_dir = tmp_path / "skills"
        (skills_dir / "skill-b").mkdir(parents=True)

        source = templates_dir / "test.md"
        source.write_text("content")

        monkeypatch.setattr(st, "TEMPLATES_DIR", templates_dir)  # type: ignore[attr-defined]
        monkeypatch.setattr(st, "SKILLS_DIR", skills_dir)  # type: ignore[attr-defined]
        monkeypatch.setattr(st, "REPO_ROOT", tmp_path)  # type: ignore[attr-defined]

        sync_template("test.md", ["skill-b"])

        assert (skills_dir / "skill-b" / "references" / "test.md").exists()

    def test_real_templates_registered(self) -> None:
        """Verify TEMPLATE_CONSUMERS has expected entries."""
        assert "detection-patterns.md" in TEMPLATE_CONSUMERS
        assert "humanize" in TEMPLATE_CONSUMERS["detection-patterns.md"]
        assert "linkedin-post-style" in TEMPLATE_CONSUMERS["detection-patterns.md"]
        assert "manuscript-review" in TEMPLATE_CONSUMERS["detection-patterns.md"]
