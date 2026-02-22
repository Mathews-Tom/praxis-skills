# Generated Skill Template

Use this template during Phase 4 (Generation) to produce the output skill.
Fill bracketed sections based on the classification and strategy from Phases 2-3.

---

## Output SKILL.md Template

```markdown
---
name: [service-name]
description: >
  [Concise description. MUST include original MCP tool names as trigger phrases,
  the service name and aliases, action verbs (search, create, list, fetch, query),
  and explicit "Use this skill when..." clause.]
---

# [Service Name]

[One-line summary of what this skill does and what it replaces.]

Replaces: [MCP server name] ([N] tools, ~[X] tokens/turn saved)

## Quick Reference

| Operation | Old MCP Tool   | New Command     |
| --------- | -------------- | --------------- |
| [op1]     | `mcp_tool_1()` | `cli command1`  |
| [op2]     | `mcp_tool_2()` | `cli command2`  |
| [op3]     | `mcp_tool_3()` | `curl endpoint` |

## Prerequisites

### Required Tools

- **[tool1]** — [purpose]. Install: `[install command]`
- **[tool2]** — [purpose]. Install: `[install command]`

### Authentication

[Auth setup — env vars, CLI login, config files]

## Core Operations

### [Operation 1 Name]

**Replaces:** `mcp_tool_name(param1, param2)`

[replacement command with parameter placeholders]

**Parameters:**

- `PARAM1` — [description] (required)
- `PARAM2` — [description] (optional, default: [value])

**Example:**

[concrete example with realistic values]

**Error handling:**

- If [condition]: [what to do]

### [Operation 2 Name]

[same pattern]

## Common Workflows

### [Workflow Name]

[Description of the multi-step pattern]

**Step 1:** [description]

[command]

**Step 2:** [description, may reference Step 1 output]

[command using previous result]

## Error Handling

| Error             | Cause                    | Fix               |
| ----------------- | ------------------------ | ----------------- |
| [error pattern]   | [why it happens]         | [how to fix]      |
| 401 Unauthorized  | Token expired or missing | Re-run auth setup |
| command not found | CLI not installed        | [install command] |

## Limitations

[Honest list of what this skill cannot do vs the original MCP]
```

---

## Sizing Guide

| MCP Size   | SKILL.md Target Lines | Use references/      |
| ---------- | --------------------- | -------------------- |
| 1-3 tools  | 50-100                | No                   |
| 4-8 tools  | 100-250               | Rarely               |
| 9-15 tools | 200-350               | For complex tools    |
| 16+ tools  | 300-500               | Yes, split by domain |

If the SKILL.md exceeds 500 lines, move detailed API patterns into
`references/api-reference.md` and keep SKILL.md focused on the most common
operations and workflows.

---

## Frontmatter Description Checklist

Verify before finalizing:

- All original MCP tool names included (verbatim, as trigger phrases)
- Service/product name and common aliases present
- Action verbs users would say (create, search, deploy, list, query)
- Explicit "Use this skill when..." clause
- Domain terms (repository, issue, container, endpoint, etc.)
- Description under 1024 characters
- No angle brackets in description

---

## Quality Checklist

Before presenting to the user:

- Every ESSENTIAL tool has a working replacement
- Every command traces through correctly (mentally test it)
- Auth uses env vars or config, never hardcoded
- Error handling covers common failure modes
- Quick Reference table is complete and accurate
- Prerequisites include install commands for every tool
- Examples use realistic values (not just placeholders)
- Limitations section is honest about gaps
- Total SKILL.md under 500 lines
- Frontmatter validates (run quick_validate.py)
