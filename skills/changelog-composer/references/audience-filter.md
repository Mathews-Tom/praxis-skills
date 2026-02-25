# Audience Filter

Rules for determining whether a change is user-facing or internal-only, and how
to adjust changelog content for different audiences.

---

## Audience Types

| Audience | What They Care About | What to Exclude |
|----------|---------------------|-----------------|
| End users | Features, bug fixes, breaking changes | Internal refactoring, test changes, CI |
| Developers (consumers) | API changes, new methods, deprecations | Internal architecture, test infrastructure |
| Contributors | Architecture changes, test infrastructure | End-user feature descriptions |

Default audience is **end users** unless specified otherwise.

---

## User-Facing Detection

### File-Based Heuristics

| Files Changed | Likely User-Facing | Rationale |
|---------------|-------------------|-----------|
| `src/**/*.py` (public modules) | Yes | Implementation changes may affect behavior |
| `tests/**` only | No | Tests don't change behavior |
| `*.md` in root | Sometimes | README changes may document new features |
| `.github/**`, `ci/**` | No | CI configuration |
| `pyproject.toml` (version only) | No | Version bump alone isn't newsworthy |
| `pyproject.toml` (deps) | Sometimes | Security-relevant dependency updates |
| `migrations/**` | Sometimes | Schema changes may indicate features |
| `docs/**` | Sometimes | New guides indicate new features |

### Content-Based Heuristics

| Commit Content | User-Facing | Rationale |
|---------------|-------------|-----------|
| Modifies public function signature | Yes | API change |
| Adds new public function/class | Yes | New capability |
| Modifies private/internal function | No | Implementation detail |
| Changes error message text | Sometimes | If users see the message |
| Modifies configuration schema | Yes | Users interact with config |
| Updates dependency version | Sometimes | Only if behavior changes or security fix |

---

## Exclusion Patterns

### Always Exclude (for end-user changelog)

- Test additions, modifications, or refactoring
- CI/CD pipeline changes
- Code style/formatting changes
- Internal refactoring with no behavior change
- Comment additions or modifications
- Type annotation additions
- Development tool configuration (linters, formatters)
- Lock file updates (unless security-relevant)

### Exclude Unless Significant

- Dependency bumps — include only if:
  - Security vulnerability fixed
  - Major version upgrade with behavior changes
  - New capability enabled
- Refactoring — include only if:
  - Public API surface changed
  - Performance characteristics changed
  - Error messages changed

### Never Exclude

- Breaking changes (regardless of how "minor")
- Security fixes
- Data loss fixes
- Privacy-related changes

---

## Multi-Audience Strategy

When the same release needs changelogs for different audiences:

### Approach: Layered Changelogs

```markdown
## [2.0.0] - 2026-02-25

### Breaking Changes
{All audiences see this}

### Features
{End users and developers see this}

### Fixes
{End users and developers see this}

### Developer Notes
{Developers and contributors see this — API changes, deprecations}

### Internal
{Contributors only — refactoring, test improvements, CI changes}
```

Use the `--audience` flag (or equivalent) to control which sections appear:
- `user` → Breaking + Features + Fixes
- `developer` → Breaking + Features + Fixes + Developer Notes
- `contributor` → Everything
