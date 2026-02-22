---
name: skill-evaluator
description: >
  Evaluate Claude Code skill quality across 6 weighted dimensions: frontmatter quality,
  trigger coverage, structural completeness, content depth, consistency and integrity,
  and CONTRIBUTING.md compliance. Produces scored audit reports with severity-classified
  findings and actionable recommendations. Two modes: (1) Quick Audit — single skill,
  full per-dimension report with weighted scoring; (2) Full Audit — all skills in repo,
  comparative ranking table plus per-skill summaries. Triggers on: "evaluate skill",
  "audit skill quality", "score skill", "skill review", "check skill completeness",
  "rate this skill", "skill quality check", "grade skill", "assess skill", "skill audit",
  "how good is this skill", or when a user asks for feedback on a SKILL.md file. Use this
  skill when reviewing skills before deployment, comparing skill quality across a repo,
  or diagnosing why a skill fails to activate on relevant queries.
metadata:
  version: 1.0.0
---

# Skill Evaluator

Skills that do not activate on relevant queries waste the entire investment in writing
them. A skill can have deep, well-structured content and still deliver zero value if its
frontmatter description lacks the trigger phrases users actually type. Quality evaluation
catches trigger gaps, missing sections, and shallow content before deployment — turning
a skill from a static document into a reliable tool.

## Reference Files

| File | Contents |
| ---- | -------- |
| `references/evaluation-rubric.md` | Detailed 1-5 scoring criteria per dimension, weight justifications, worked examples for calibration |

## Audit Modes

Two modes, selected by input:

- **Quick Audit**: Evaluate a single skill. Produces a full per-dimension scored report
  with findings, severity classifications, and recommendations.
- **Full Audit**: Evaluate all skills in the repository. Produces a comparative ranking
  table sorted by overall score, plus condensed per-skill summaries.

### Mode Selection

| Input | Mode |
| ----- | ---- |
| Path to a specific skill directory or SKILL.md | Quick Audit |
| "all", "every skill", no path specified, or repo-level request | Full Audit |
| Multiple specific paths | Quick Audit for each, then comparative summary |

---

## Evaluation Dimensions

Six dimensions, each scored 1-5. Weighted sum determines overall percentage.

### D1: Frontmatter Quality (20%)

Evaluates the YAML frontmatter block for completeness and discoverability.

**Signals:**
- `name` field present and non-empty
- `description` field present and non-empty
- Description length between 200-800 characters (sweet spot for keyword density without bloat)
- Description contains explicit trigger phrases users would type
- Description includes a "Use this skill when..." clause or equivalent
- Description is keyword-dense, not generic filler

**Scoring constraints:** A description under 100 characters caps this dimension at 2/5.
A missing `name` or `description` field caps at 1/5.

### D2: Trigger Coverage (18%)

Evaluates whether the skill activates on the queries users actually type.

**Signals:**
- Synonym breadth — multiple phrasings for the same intent (e.g., "review", "audit",
  "critique", "evaluate", "assess", "check")
- Implied contexts — situations where the skill applies even without explicit keywords
  (e.g., "user provides a design doc and asks for feedback")
- Domain-specific terms relevant to the skill's function
- Explicit trigger phrase list in the description frontmatter
- Coverage of both imperative ("review this") and interrogative ("is this good?") forms

**Scoring constraints:** Fewer than 3 distinct trigger phrases caps at 2/5. Zero trigger
phrases in the description caps at 1/5.

### D3: Structural Completeness (20%)

Evaluates whether the skill contains the sections needed to function reliably.

**Signals:**
- Prerequisites or setup instructions (if applicable)
- Multi-phase workflow or step-by-step procedure
- Error handling guidance or edge case documentation
- Output format specification (template, example, or schema)
- Limitations or scope boundaries stated
- Reference file table (if references/ directory exists)
- Calibration rules or quality gates

**Scoring constraints:** A skill with no workflow section caps at 2/5. A skill with
a workflow but no error handling or output format caps at 3/5.

### D4: Content Depth (22%)

Evaluates the substantive quality of the skill's guidance — whether it provides enough
detail for an agent to execute well without human intervention.

**Signals:**
- Multi-step workflows with decision points, not bare command lists
- Error cases documented with recovery actions
- Decision frameworks (when to do X vs Y, mode selection tables)
- Verbatim output examples or templates
- Severity classifications or scoring rubrics (where applicable)
- Cross-cutting analysis or synthesis steps beyond simple checklists

**Scoring constraints:** A skill consisting only of bare commands with no explanatory
context caps at 2/5. Reference files count toward this dimension only if they contain
substantive guidance (checklists, rubrics, criteria), not just link collections.

### D5: Consistency and Integrity (12%)

Evaluates internal consistency and structural integrity.

**Signals:**
- Directory name matches the `name` field in frontmatter exactly
- All files referenced in SKILL.md exist on disk (reference files, scripts, assets)
- Description content aligns with body content (description does not promise features
  the body does not deliver)
- Consistent terminology throughout (same concept uses same term)
- No broken internal links or dangling references

**Scoring constraints:** A name mismatch between directory and frontmatter is a CRITICAL
finding and caps at 1/5. Missing referenced files cap at 2/5.

### D6: CONTRIBUTING.md Compliance (8%)

Evaluates adherence to the repository's contribution guidelines.

**Signals:**
- Skill name is kebab-case
- Skill name is 64 characters or fewer
- Description is 1024 characters or fewer
- No angle brackets in description
- No pushy trigger language in description ("always use", "you must", "never do")
- Valid YAML frontmatter syntax

**Scoring constraints:** Any single violation caps at 3/5. Multiple violations cap at 2/5.
Invalid YAML that prevents parsing caps at 1/5.

---

## Severity Classification

| Severity | Criteria | Score Impact |
| -------- | -------- | ------------ |
| CRITICAL | Skill cannot activate or breaks on load — missing frontmatter, name mismatch, invalid YAML | Caps overall score at 40% |
| HIGH | Significant trigger gap or missing core section — no workflow, no error handling, zero trigger phrases | Caps affected dimension at 3/5 |
| MEDIUM | Weak coverage, shallow content, few trigger synonyms | Dimension needs improvement but functions |
| LOW | Minor polish — formatting inconsistencies, slightly short description, missing calibration rules | Fix when convenient |

---

## Workflow

### Phase 1: Input

1. Determine audit mode from user input (see Mode Selection table above).
2. For Quick Audit: validate the skill directory exists and contains a `SKILL.md` file.
   If the path points to a SKILL.md directly, use its parent directory.
3. For Full Audit: enumerate all directories under `skills/` that contain a `SKILL.md`.
4. For each skill to evaluate, note the directory name for D5 consistency checks.

### Phase 2: Analysis

For each skill under evaluation:

1. Read `SKILL.md` in full.
2. Parse YAML frontmatter — extract `name` and `description` fields. If YAML parsing
   fails, record a CRITICAL finding and score D1 and D6 as 1/5.
3. Check the `references/` directory for existence and contents. Verify every file
   referenced in the SKILL.md body exists on disk.
4. Evaluate each of the 6 dimensions using the criteria above and the detailed rubric
   in `references/evaluation-rubric.md`.
5. Record findings with severity, dimension tag, description, and recommendation.

### Phase 3: Scoring

1. Score each dimension 1-5 using `references/evaluation-rubric.md`.
2. Apply severity caps: if any CRITICAL finding exists, cap overall at 40% regardless
   of dimension scores.
3. Compute weighted score: `Overall% = (sum of dimension_score x weight) / 5 x 100`.
4. Determine verdict from the scale below.

| Range | Verdict |
| ----- | ------- |
| 90-100% | Exemplary |
| 80-89% | Strong |
| 70-79% | Adequate |
| 60-69% | Needs Work |
| Below 60% | Deficient |

### Phase 4: Report

Generate the structured output using the appropriate template below.

---

## Output Format

### Quick Audit Template

```text
## Skill Audit: {skill-name}

| Dimension | Score | Weight | Weighted | Key Finding |
|-----------|-------|--------|----------|-------------|
| D1: Frontmatter Quality | X/5 | 20% | X.XXX | ... |
| D2: Trigger Coverage | X/5 | 18% | X.XXX | ... |
| D3: Structural Completeness | X/5 | 20% | X.XXX | ... |
| D4: Content Depth | X/5 | 22% | X.XXX | ... |
| D5: Consistency & Integrity | X/5 | 12% | X.XXX | ... |
| D6: CONTRIBUTING Compliance | X/5 | 8% | X.XXX | ... |

**Overall: XX% — {Verdict}**

### Findings

[Severity-sorted list. Each entry includes dimension tag, severity, description,
evidence, and recommendation.]

- **[CRITICAL] D5:** ...
- **[HIGH] D2:** ...
- **[MEDIUM] D4:** ...
- **[LOW] D3:** ...

### Score Calculation

D1: {score} x 0.20 = {result}
D2: {score} x 0.18 = {result}
D3: {score} x 0.20 = {result}
D4: {score} x 0.22 = {result}
D5: {score} x 0.12 = {result}
D6: {score} x 0.08 = {result}
Sum = {weighted_sum}
Overall = {weighted_sum} / 5 x 100 = {percentage}% — {Verdict}
```

### Full Audit Template

```text
## Skill Repository Audit

| Skill | Overall | Verdict | Worst Dimension | Top Issue |
|-------|---------|---------|-----------------|-----------|
| {name} | XX% | {verdict} | {dimension} | {issue} |
| ... | ... | ... | ... | ... |

### Per-Skill Summaries

[Condensed Quick Audit for each skill: scorecard table, overall score, top 3 findings.
Omit the full Score Calculation section in condensed mode.]
```

---

## Error Handling

| Problem | Cause | Fix |
| ------- | ----- | --- |
| `SKILL.md` not found in directory | Path incorrect or file missing | Report as CRITICAL; do not attempt evaluation; surface the path and stop |
| YAML frontmatter parse failure | Invalid YAML syntax (unclosed quotes, bad indentation) | Report as CRITICAL finding; score D1 and D6 as 1/5; continue evaluating the body content where parseable |
| `references/` directory missing | Skill has no reference files | Not an error — score D5 normally; check only that any files referenced in the SKILL.md body actually exist on disk |
| `references/` exists but referenced file is absent | File path in SKILL.md body doesn't resolve | Record as a CRITICAL D5 finding; missing referenced files cap D5 at 2/5 |
| Empty `SKILL.md` (zero bytes or whitespace only) | File created but never populated | Treat as CRITICAL; score all dimensions 1/5; overall verdict: Deficient |
| `references/evaluation-rubric.md` not found | Skill's own reference file missing | Note the irony; evaluate using the criteria inline in this SKILL.md; flag D5 as a CRITICAL finding |

## Calibration Rules

1. Score what exists, not what could exist — evaluate the skill as-is, not its potential.
2. Weight trigger coverage heavily for skills targeting broad domains (e.g., a GitHub skill
   covers issues, PRs, CI, releases, and API — it needs proportionally more trigger synonyms).
3. A skill with strong triggers but shallow content scores higher than deep content with
   poor triggers — activation is prerequisite to utility.
4. Reference files count toward Content Depth only if they contain substantive guidance
   (checklists, rubrics, criteria), not link lists or stub files.
5. When evaluating the skill-evaluator itself, apply identical standards — no self-inflation.
6. Frontmatter description quality is the single highest-leverage improvement for any skill.
