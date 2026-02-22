# Replacement Patterns Reference

Detailed replacement patterns for each MCP tool category. Load this reference
during Phase 3 (Replacement Strategy) of the conversion workflow.

## Table of Contents

1. [REST API Wrappers](#rest-api-wrappers)
2. [CLI Wrappers](#cli-wrappers)
3. [Logic and Reasoning Patterns](#logic-and-reasoning-patterns)
4. [File Operations](#file-operations)
5. [Stateful Operations](#stateful-operations)
6. [Composite Operations](#composite-operations)
7. [Auth Patterns](#auth-patterns)
8. [Output Parsing Patterns](#output-parsing-patterns)

---

## REST API Wrappers

Most MCP servers are thin wrappers around REST APIs. Replace with `curl` or
`web_fetch` using the right headers and parameters.

### Simple GET

```markdown
### Operation Name

**Replaces:** `mcp_tool_name(param1, param2)`

\`\`\`bash
curl -s "https://api.service.com/v1/endpoint?param1=VALUE&param2=VALUE" \
 -H "Authorization: Bearer $SERVICE_API_KEY" \
 -H "Content-Type: application/json" | jq '.data'
\`\`\`

**Parameters:**

- `param1` — Description (required)
- `param2` — Description (optional, default: "value")

**Example:**
\`\`\`bash
curl -s "https://api.service.com/v1/users?role=admin" \
 -H "Authorization: Bearer $SERVICE_API_KEY" | jq '.users[] | {name, email}'
\`\`\`
```

### POST with Body

```markdown
### Operation Name

**Replaces:** `mcp_tool_name(data)`

\`\`\`bash
curl -s -X POST "https://api.service.com/v1/endpoint" \
 -H "Authorization: Bearer $SERVICE_API_KEY" \
 -H "Content-Type: application/json" \
 -d '{
"field1": "VALUE",
"field2": VALUE
}' | jq '.'
\`\`\`
```

### Paginated Results

```markdown
### Operation Name (paginated)

**Replaces:** `mcp_tool_name(query, page, per_page)`

\`\`\`bash

# First page

curl -s "https://api.service.com/v1/search?q=QUERY&page=1&per_page=20" \
 -H "Authorization: Bearer $SERVICE_API_KEY" | jq '.'

# Check response for next_page or total_pages to continue

\`\`\`

Pipe through `jq` to extract only needed fields and reduce output size for
large result sets.
```

### Using web_fetch (Claude.ai)

When operating in Claude.ai where `web_fetch` is a native tool:

```markdown
### Operation Name

**Replaces:** `mcp_tool_name(param)`

Use web_fetch to retrieve: `https://api.service.com/v1/endpoint?param=VALUE`

Note: web_fetch may not support custom auth headers. For authenticated APIs,
prefer curl via bash.
```

---

## CLI Wrappers

Many MCPs wrap CLI tools that are already installed or easily installable.
Replace with direct CLI invocation — often more powerful than the MCP since
you get the full CLI feature set instead of a subset exposed as tools.

### Common CLI Mappings

| Service      | MCP Tools                                        | CLI Replacement | Install                         |
| ------------ | ------------------------------------------------ | --------------- | ------------------------------- |
| GitHub       | create_issue, list_repos, create_pr, search_code | `gh`            | `brew install gh`               |
| AWS          | s3_upload, lambda_invoke, ec2_list               | `aws`           | `brew install awscli`           |
| Google Cloud | gcs_upload, run_query                            | `gcloud` / `bq` | `brew install google-cloud-sdk` |
| Docker       | container_list, image_build                      | `docker`        | Docker Desktop                  |
| Kubernetes   | pod_list, apply_manifest                         | `kubectl`       | `brew install kubectl`          |
| Git          | commit, push, diff, log                          | `git`           | Pre-installed                   |
| npm/Node     | package_info, run_script                         | `npm` / `npx`   | Pre-installed with Node         |
| Postgres     | query, list_tables                               | `psql`          | `brew install postgresql`       |

### CLI Replacement Pattern

```markdown
### Operation Name

**Replaces:** `mcp_tool_name(param1, param2)`

\`\`\`bash
cli-tool subcommand --flag1 VALUE1 --flag2 VALUE2
\`\`\`

**Parameter mapping:**
| MCP Param | CLI Flag | Notes |
|-----------|----------|-------|
| `param1` | `--flag1` | Required |
| `param2` | `--flag2` | Optional |

**Example:**
\`\`\`bash
gh issue create --title "Bug: login fails" --body "Steps to reproduce..." --label bug
\`\`\`
```

### CLI with JSON Output

Many CLIs support JSON output for structured parsing:

```bash
gh api repos/{owner}/{repo}/issues --jq '.[].title'
gh issue list --json number,title,state --jq '.[] | "\(.number): \(.title) [\(.state)]"'
kubectl get pods -o json | jq '.items[] | {name: .metadata.name, status: .status.phase}'
aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId' --output text
```

---

## Logic and Reasoning Patterns

Some MCP tools don't call external services — they structure Claude's own
reasoning via self-directed tool calls. Convert these to instructional methodology.

The key insight: these tools are expensive forcing functions (~1500-2000 tokens of
schema) for something Claude can do natively when instructed. A well-written
methodology section achieves the same structured reasoning at zero token cost until
the skill is loaded.

### Structured Reasoning (e.g., Sequential Thinking)

```markdown
## Structured Problem Solving

When facing complex, multi-step problems:

1. **Scope assessment** — Estimate steps needed. State: "This requires ~N steps."

2. **Step-by-step execution** — Work through each step explicitly:
   - Number each step
   - State the sub-goal
   - Show the work
   - State the conclusion before moving on

3. **Revision checkpoints** — After every 3-4 steps, pause:
   - "Am I still on the right track?"
   - "Do any earlier conclusions need revision?"
   - If revising: "Revising step N because..."

4. **Branch exploration** — When multiple approaches exist:
   - Label: "Approach A: ...", "Approach B: ..."
   - Evaluate each briefly, then commit with rationale

5. **Verification** — Before concluding:
   - Restate the original problem
   - Verify the solution satisfies all constraints
   - Flag remaining uncertainties
```

### Planning and Task Decomposition

```markdown
## Task Planning

Before executing complex tasks:

1. Break into subtasks (aim for 3-7 items)
2. Identify dependencies between subtasks
3. Flag risks or unknowns for each
4. Execute in dependency order
5. After each subtask, verify output before proceeding
```

---

## File Operations

MCP tools that read, write, or transform files map directly to bash commands
or small Python scripts.

### Common Mappings

| MCP Operation                 | Bash Replacement                                |
| ----------------------------- | ----------------------------------------------- |
| `read_file(path)`             | `cat path` or `head -n 100 path`                |
| `write_file(path, content)`   | `echo "content" > path` or heredoc              |
| `list_directory(path)`        | `ls -la path` or `find path -maxdepth 1`        |
| `search_files(pattern, path)` | `grep -r "pattern" path` or `rg "pattern" path` |
| `file_info(path)`             | `stat path` or `wc -l path`                     |
| `move_file(src, dst)`         | `mv src dst`                                    |
| `copy_file(src, dst)`         | `cp src dst`                                    |

### Complex File Transforms

For transforms beyond simple bash:

```markdown
### Transform Name

**Replaces:** `mcp_transform(input_path, options)`

\`\`\`bash
python3 -c "
import json
with open('INPUT_PATH') as f:
data = json.load(f)
result = transform(data)
with open('OUTPUT_PATH', 'w') as f:
json.dump(result, f, indent=2)
"
\`\`\`
```

---

## Stateful Operations

These are the hardest to convert. Stateful MCP tools maintain server-side state
(database connections, sessions, caches, subscriptions).

### Assessment Questions

Before attempting conversion, ask:

1. Does the tool maintain a persistent connection? (DB, WebSocket)
2. Does the tool cache data between calls?
3. Do multiple tools share state?
4. Is there a stateless alternative?

### Stateless Equivalent (when possible)

```markdown
### Operation Name

**Replaces:** `mcp_query(sql)` (which used a persistent connection)

\`\`\`bash
psql "$DATABASE_URL" -c "SELECT \* FROM users WHERE active = true" --csv
\`\`\`

Trade-off: slightly higher latency per call (connection overhead), but
eliminates state management entirely.
```

### Script-Based State (when stateless is not possible)

```markdown
### Operation Name

**Replaces:** `mcp_stateful_op(params)`

\`\`\`bash
python3 scripts/stateful_helper.py --action ACTION --params PARAMS
\`\`\`

The script manages state via a local file or SQLite database.
```

### When to Recommend Keeping the MCP

If the tool genuinely requires persistent state that can't be replicated:

> "These tools maintain persistent [connections/sessions/caches] that can't
> be cleanly replaced with stateless commands. Recommend keeping as a standalone
> MCP — it's only N tokens of context overhead."

---

## Composite Operations

MCP tools that orchestrate multiple sub-operations become workflow sections.

### Multi-Step Workflow Pattern

```markdown
## Workflow: Name

**Replaces:** `mcp_composite_tool(params)` which internally did steps 1-3

### Step 1: First Operation

\`\`\`bash
RESULT=$(command1 --param VALUE)
\`\`\`

### Step 2: Second Operation (uses Step 1 output)

\`\`\`bash
command2 --input "$RESULT" --flag VALUE
\`\`\`

### Step 3: Final Operation

\`\`\`bash
command3 --finalize
\`\`\`
```

---

## Auth Patterns

### Environment Variables (Preferred)

```markdown
## Prerequisites

Set these environment variables:

\`\`\`bash
export SERVICE_API_KEY="your-api-key-here"
export SERVICE_BASE_URL="https://api.service.com" # optional, has default
\`\`\`

Claude Code: Add to shell profile (~/.zshrc, ~/.bashrc)
Claude.ai: Set via bash at session start
```

### CLI Tool Auth

```markdown
## Prerequisites

Authenticate the CLI tool:

\`\`\`bash
gh auth login # GitHub CLI
aws configure # AWS CLI
gcloud auth login # Google Cloud CLI
\`\`\`
```

### Token Check Pattern

```bash
# Verify auth is configured before running commands
if [ -z "$GITHUB_TOKEN" ]; then
  echo "Error: GITHUB_TOKEN not set. Run: export GITHUB_TOKEN=your-token"
  exit 1
fi
```

---

## Output Parsing Patterns

### jq for JSON APIs

```bash
# Extract specific field
curl -s URL | jq '.field'

# Filter array
curl -s URL | jq '.items[] | select(.status == "active")'

# Format as table
curl -s URL | jq -r '.items[] | [.name, .status] | @tsv'

# Count results
curl -s URL | jq '.items | length'
```

### CLI Native Formatting

```bash
# GitHub CLI: built-in JSON + jq
gh issue list --json number,title --jq '.[] | "\(.number): \(.title)"'

# kubectl: Go templates
kubectl get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'

# AWS CLI: query parameter
aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId' --output text
```

### Python for Complex Parsing

```bash
python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
for item in data['results']:
    print(f\"{item['name']}: {item['score']:.2f}\")
" <<< "$(curl -s URL)"
```
