# Conventional Commits

Parsing rules for the Conventional Commits specification (v1.0.0). Extract type, scope,
description, and breaking change indicators from commit messages.

---

## Format

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

### Type Mapping

| Type | Category | User-Facing |
|------|----------|-------------|
| `feat` | Feature | Yes |
| `fix` | Fix | Yes |
| `perf` | Performance | Yes |
| `docs` | Documentation | Sometimes |
| `refactor` | Internal | No (usually) |
| `test` | Internal | No |
| `chore` | Internal | No |
| `ci` | Internal | No |
| `build` | Internal | No |
| `style` | Internal | No |
| `revert` | Depends on reverted commit | Depends |

### Breaking Change Indicators

A commit is a breaking change if ANY of these are present:

1. `!` after the type/scope: `feat!: remove deprecated API`
2. `BREAKING CHANGE:` in the footer:
   ```
   feat: new auth system

   BREAKING CHANGE: token format changed from JWT to opaque
   ```
3. `BREAKING-CHANGE:` (hyphenated variant) in the footer

### Scope

The scope is a noun describing the section of the codebase:

```
feat(auth): add OAuth2 support
fix(parser): handle empty input
perf(cache): reduce memory allocation
```

Common scopes: `api`, `auth`, `cli`, `config`, `core`, `db`, `deps`, `docs`, `ui`

---

## Parsing Rules

### Extract Type

```python
import re

CONVENTIONAL_PATTERN = re.compile(
    r'^(?P<type>\w+)'          # type
    r'(?:\((?P<scope>[^)]+)\))?' # optional (scope)
    r'(?P<breaking>!)?'        # optional ! for breaking
    r':\s*'                    # colon separator
    r'(?P<description>.+)$'   # description
)

def parse_commit(message: str) -> dict | None:
    first_line = message.split('\n')[0]
    match = CONVENTIONAL_PATTERN.match(first_line)
    if not match:
        return None

    body = '\n'.join(message.split('\n')[1:])
    is_breaking = (
        match.group('breaking') == '!' or
        'BREAKING CHANGE:' in body or
        'BREAKING-CHANGE:' in body
    )

    return {
        'type': match.group('type'),
        'scope': match.group('scope'),
        'breaking': is_breaking,
        'description': match.group('description'),
    }
```

### Non-Conventional Commit Heuristics

When commits don't follow the convention, classify by keywords:

| Keyword Pattern | Likely Category |
|----------------|-----------------|
| "add", "implement", "introduce", "support" | Feature |
| "fix", "resolve", "correct", "patch", "repair" | Fix |
| "speed", "faster", "optimize", "reduce memory" | Performance |
| "doc", "readme", "comment", "guide" | Documentation |
| "refactor", "clean", "restructure", "rename" | Internal |
| "update dep", "bump", "upgrade" | Dependency (internal unless security) |
| "test", "spec", "coverage" | Internal |
| "ci", "pipeline", "workflow", "action" | Internal |
| "remove", "delete", "drop", "deprecate" | Potentially breaking |

---

## Edge Cases

### Revert Commits

```
revert: feat(auth): add OAuth2 support

This reverts commit abc1234.
```

A revert of a feature is effectively a breaking change if the feature was released.
A revert of a fix re-introduces the bug. Classify based on what was reverted.

### Merge Commits

Merge commits (e.g., `Merge pull request #123 from branch`) are not conventional
commits. Skip them and parse the individual commits within the PR instead.

### Multi-Line Descriptions

The first line is the description. The body (after a blank line) provides additional
detail but is not the primary changelog entry. Use the first line for the changelog;
reference the body for breaking change details.

### Missing Type

If a commit has no recognizable type prefix, it's unclassified. Default to "Internal"
unless the changed files clearly indicate user-facing impact (e.g., public API files
were modified).
