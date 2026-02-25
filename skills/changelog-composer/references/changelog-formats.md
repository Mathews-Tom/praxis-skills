# Changelog Formats

Templates for different changelog output formats: Keep a Changelog, GitHub Releases,
and announcement copy.

---

## Keep a Changelog (CHANGELOG.md)

The standard format for `CHANGELOG.md` files. Based on https://keepachangelog.com.

### Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-02-25

### Added
- New feature description. ([#123](url))

### Changed
- Modified behavior description. ([#124](url))

### Deprecated
- Feature X is deprecated and will be removed in v2.0.

### Removed
- Removed deprecated function Y. ([#125](url))

### Fixed
- Fixed crash when processing empty input. ([#126](url))

### Security
- Updated dependency Z to fix CVE-XXXX-XXXX. ([#127](url))

## [1.1.0] - 2026-01-15
...

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
```

### Category Mapping

| Keep a Changelog | Our Category |
|-----------------|--------------|
| Added | Features |
| Changed | Breaking Changes (behavioral) |
| Deprecated | (include in Features or Breaking) |
| Removed | Breaking Changes (removal) |
| Fixed | Fixes |
| Security | Security (subset of Fixes) |

### Rules

1. Newest version at the top
2. `[Unreleased]` section always present for in-progress changes
3. Dates in ISO 8601 format (YYYY-MM-DD)
4. Version links at the bottom comparing tags
5. Entries written in imperative mood ("Add", not "Added" or "Adds")

---

## GitHub Release Notes

Format for GitHub's release feature (`gh release create`).

### Structure

```markdown
## What's New

### Breaking Changes ⚠️
- **`function_name` parameter renamed** — `old` → `new`. See migration guide. (#123)

### Features ✨
- **Feature name** — description of what's new. (#124)

### Bug Fixes 🐛
- Fixed issue where X happened under Y conditions. (#125)

### Performance ⚡
- Improved Z processing speed by 40%. (#126)

**Full Changelog**: https://github.com/user/repo/compare/v1.1.0...v1.2.0
```

### Differences from CHANGELOG.md

- Uses emoji prefixes for visual scanning
- More conversational tone
- Includes "Full Changelog" compare link
- May include contributor acknowledgments
- Single release, not cumulative

---

## Announcement Copy

For blog posts, social media, or team communication.

### Structure

```markdown
# {Project} v{X.Y.Z} Released

{One sentence summary of the most important change.}

## Highlights

- **{Top feature}** — {what it means for users, 1-2 sentences}
- **{Second feature}** — {what it means for users}
- **{Important fix}** — {what was broken and is now fixed}

## Breaking Changes

{If any, explain what users need to do to upgrade.}

## Get Started

```bash
pip install project==X.Y.Z
```

Full changelog: {link}
```

### Writing Guidelines

- Lead with the most impactful change
- Maximum 3-5 highlights — this is a summary, not the full changelog
- Use benefit-oriented language ("You can now..." not "We implemented...")
- Include upgrade command or link
- Link to full changelog for details

---

## Format Selection Guide

| Context | Format | Reasoning |
|---------|--------|-----------|
| Repository CHANGELOG.md | Keep a Changelog | Standard, cumulative, versioned |
| GitHub release | GitHub Release Notes | Visual, single-release, linkable |
| Team Slack/email | Announcement Copy | Brief, highlights only |
| User documentation | Keep a Changelog variant | Detailed, searchable |
| Marketing blog | Announcement Copy | Benefit-oriented, non-technical |
