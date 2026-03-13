# Contributing

## Skill Structure

Each skill lives in its own directory under `skills/` and must contain a `SKILL.md` file.

`SKILL.md` requires YAML frontmatter:

```yaml
---
name: my-skill-name
description: What this skill does in plain language.
metadata:
  version: 1.0.0
---
```

Optional subdirectories:

- `references/` — documents or context files the skill uses
- `scripts/` — helper scripts invoked by the skill
- `assets/` — images or static files

## Versioning

Skills use [semantic versioning](https://semver.org/) via the `metadata.version` field in SKILL.md frontmatter.

| Change Type | Bump | Example |
|-------------|------|---------|
| Breaking change to skill interface or behavior | MAJOR | `1.0.0` → `2.0.0` |
| New capability, backward-compatible | MINOR | `1.0.0` → `1.1.0` |
| Bug fix, typo, clarification | PATCH | `1.0.0` → `1.0.1` |

After changing a version, regenerate the manifest:

```bash
uv run scripts/generate_manifest.py
```

## Naming Rules

- Skill names: kebab-case, maximum 64 characters
- Directory name must match the `name` field in frontmatter

## Self-Containment

Skills must be standalone packages. Every file a skill references must live within its own directory.

**Blocked:**
- `../other-skill/references/file.md` — cross-skill path references
- Absolute paths to files outside the skill directory
- References to files that only exist in other skills

**Why:** Skills are distributed individually via `npx skills add` and `.skill` archives. Cross-skill references break when a skill is installed without its dependency. The skill-evaluator flags this as a CRITICAL D5 finding.

**Shared content:** If multiple skills need the same reference file, use the template sync system (see below). Each skill gets its own physical copy, managed by `scripts/sync_templates.py`.

## Shared Templates

The `_templates/` directory holds reference files shared across multiple skills. The sync system copies templates into each consuming skill's `references/` directory.

**How it works:**

1. Source files live in `_templates/` (e.g., `_templates/detection-patterns.md`)
2. `scripts/sync_templates.py` defines which skills consume each template via `TEMPLATE_CONSUMERS`
3. Running the script copies templates to `skills/{consumer}/references/{template}`
4. A pre-commit hook runs sync automatically when templates or references change

**To add a shared template:**

1. Create the file in `_templates/`
2. Add the template name and consumer list to `TEMPLATE_CONSUMERS` in `scripts/sync_templates.py`
3. Run `uv run python scripts/sync_templates.py` to populate copies
4. Commit both the template and the synced copies

**To use an existing template in a new skill:**

1. Add your skill name to the consumer list in `scripts/sync_templates.py`
2. Run `uv run python scripts/sync_templates.py`
3. Reference the file as `references/{template}` in your SKILL.md (local path, not `../`)

Current templates:

| Template | Consumers | Purpose |
|----------|-----------|---------|
| `detection-patterns.md` | humanize, linkedin-post-style, manuscript-review | AI writing detection patterns |
| `project-detection.md` | ship-workflow, plan-review, qa-systematic | Stack-agnostic project detection |

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

## Eval Cases

Every skill must have eval cases in `skills/<name>/evals/cases.yaml`. These define trigger accuracy — does the skill activate on the right queries and stay silent on the wrong ones?

**Schema:**

```yaml
cases:
  - id: unique_snake_case_id
    prompt: "What the user would type"
    fixtures: []
    rubric:
      - "Expected behavior point 1"
      - "Expected behavior point 2"
    trigger_expected: true  # or false
```

**Requirements:**

| Skill Status | Positive Cases (trigger_expected: true) | Negative Cases (trigger_expected: false) |
|-------------|----------------------------------------|------------------------------------------|
| Active | 1+ (recommended: 2+) | 2+ |
| Deprecated | 0 (must be zero) | 2+ |

**Guidelines:**
- Positive cases should use natural language a real user would type
- Negative cases should test plausible but incorrect triggers (adjacent tasks the skill should NOT handle)
- Each case needs a unique `id` (snake_case)
- Rubric items describe what a correct response looks like, not implementation details

**Validation:**

```bash
uv run python scripts/validate_evals.py
```

CI runs this on every PR. Skills without valid evals will fail the pipeline.

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

- [ ] `SKILL.md` has valid YAML frontmatter with `name`, `description`, and `metadata.version`
- [ ] Version bumped according to semver (MAJOR/MINOR/PATCH)
- [ ] Manifest regenerated: `uv run scripts/generate_manifest.py`
- [ ] Skill name is kebab-case, under 64 characters
- [ ] Description is 200-1024 characters with trigger phrases and "Use when" clause
- [ ] No angle brackets or pushy language in description
- [ ] No secrets, credentials, or internal URLs in any file
- [ ] Tested locally with Claude Code
- [ ] All file references in `SKILL.md` resolve to existing files within the skill directory
- [ ] No cross-skill references (`../other-skill/`) — skill is fully self-contained
- [ ] Eval cases exist in `evals/cases.yaml` with 1+ positive and 2+ negative triggers
- [ ] Evals pass: `uv run python scripts/validate_evals.py`
- [ ] Templates synced (if using shared templates): `uv run python scripts/sync_templates.py`
- [ ] Skill evaluator score is 70% or above (paste the scorecard in your PR)
- [ ] No CRITICAL or HIGH findings from skill evaluator
