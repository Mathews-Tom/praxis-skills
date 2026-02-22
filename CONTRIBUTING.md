# Contributing

## Skill Structure

Each skill lives in its own directory under `skills/` and must contain a `SKILL.md` file.

`SKILL.md` requires YAML frontmatter:

```yaml
---
name: my-skill-name
description: What this skill does in plain language.
---
```

Optional subdirectories:

- `references/` — documents or context files the skill uses
- `scripts/` — helper scripts invoked by the skill
- `assets/` — images or static files

## Naming Rules

- Skill names: kebab-case, maximum 64 characters
- Directory name must match the `name` field in frontmatter

## Description Rules

- Maximum 1024 characters (sweet spot: 200-800 characters)
- No angle brackets (`<`, `>`)
- No pushy trigger language ("always use", "you must", "never do")
- Include trigger phrases users would type to activate the skill
- Include a "Use this skill when..." clause describing activation contexts

## Writing an Effective Description

The frontmatter description controls whether Claude activates your skill. A skill with deep content but a weak description delivers zero value.

**Include in every description:**

1. What the skill does (functional summary)
2. Key operations or subcommands covered
3. Trigger phrases across synonym families (e.g., "review", "audit", "critique", "evaluate")
4. A "Use this skill when..." clause listing concrete activation scenarios
5. Domain-specific terms users associate with the task

**Example (good):**

```yaml
description: >
  Architecture reviews across 7 dimensions: structural integrity, scalability,
  security, performance, enterprise readiness, operational excellence, and data
  architecture. Produces scored reports with prioritized recommendations.
  Triggers on: "review architecture", "critique design", "audit system",
  "evaluate codebase", "assess scalability". Use this skill when the user
  provides a system design document or codebase and asks for feedback.
```

**Example (insufficient):**

```yaml
description: "Review architecture and provide feedback."
```

## Quality Gate — Skill Evaluator

Before submitting a PR, run the [skill-evaluator](skills/skill-evaluator/) against your skill:

```bash
claude --add-dir skills/skill-evaluator --add-dir skills/my-skill-name
# Then: "Run a quick audit on skills/my-skill-name"
```

The evaluator scores 6 dimensions:

| Dimension                   | Weight | Minimum for PR |
| --------------------------- | ------ | -------------- |
| D1: Frontmatter Quality     | 20%    | 3/5            |
| D2: Trigger Coverage        | 18%    | 3/5            |
| D3: Structural Completeness | 20%    | 3/5            |
| D4: Content Depth           | 22%    | 3/5            |
| D5: Consistency & Integrity | 12%    | 4/5            |
| D6: CONTRIBUTING Compliance | 8%     | 4/5            |

**Minimum overall score for PR acceptance: 70% (Adequate).**

Skills scoring below 70% need improvement before review. Skills with CRITICAL findings (missing frontmatter, name mismatch) are automatically rejected.

## Testing Locally

Point Claude Code at the skill directory:

```bash
claude --add-dir skills/my-skill-name
```

Verify the skill loads and behaves as expected before submitting a PR.

## Packaging

Run the packaging script to produce a `.skill` artifact:

```bash
uv run scripts/package_skill.py skills/my-skill-name
```

## Pull Request Checklist

Before opening a PR, confirm:

- [ ] `SKILL.md` has valid YAML frontmatter with `name` and `description`
- [ ] Skill name is kebab-case, under 64 characters
- [ ] Description is 200-1024 characters with trigger phrases and "Use when" clause
- [ ] No angle brackets or pushy language in description
- [ ] No secrets, credentials, or internal URLs in any file
- [ ] Tested locally with Claude Code
- [ ] All file references in `SKILL.md` resolve to existing files
- [ ] Skill evaluator score is 70% or above (paste the scorecard in your PR)
- [ ] No CRITICAL or HIGH findings from skill evaluator
