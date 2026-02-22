# Environment Guide

Environment-specific constraints and available primitives. Load during Phase 3
when the user's target environment needs special handling.

## Environment Matrix

### Claude.ai (Web/Desktop/Mobile)

**Available primitives:** bash (full Ubuntu 24), curl, wget, python3 (with pip),
node/npm, jq, web_fetch (native tool), web_search (native tool), file tools
(view, str_replace, create_file, bash_tool).

**Limitations:** Network egress restricted to allowlisted domains. Filesystem
resets between conversations. No persistent background processes.

**Skill placement:** Platform-dependent. See the agent's skill directory configuration.

**Best for:** Skills using curl, python3, or bash. Most REST API and CLI wrapper
conversions work here.

### Claude Code (Terminal)

**Available primitives:** Full access to user's local machine. All installed CLI
tools. All programming languages. File system persistence. Background processes.
Network access (typically unrestricted).

**Skill placement:** Project `.claude/skills/` or global `~/.claude/skills/`

**Best for:** All conversion types. CLI wrappers especially benefit since the
tools are already installed locally.

### Cursor / Windsurf / IDE Agents

**Available primitives:** Bash (may be restricted), file read/write, some have
built-in terminal access. May have their own MCP config format.

**Limitations:** Network access may be restricted. Tool availability varies.
Skill loading mechanism differs by IDE.

**Best for:** File operation and CLI wrapper conversions. Verify curl availability
for REST API conversions.

### API (Custom Implementations)

**Available primitives:** Depends on implementation. Typically bash + file ops.
May or may not have network access.

**Best for:** Generate with bash + curl assumption, let user adapt.

## Environment Detection

During Phase 1, detect the environment:

1. Tools include `bash_tool`, `view`, `create_file` -> Claude.ai
2. User mentions "Claude Code" or "terminal" -> Claude Code
3. User mentions "Cursor" or "Windsurf" -> IDE agent
4. Unclear -> Ask: "Which environment will you use this skill in?"

## CLI Installation Quick Reference

| Tool      | macOS                           | Linux (apt)                     | Purpose         |
| --------- | ------------------------------- | ------------------------------- | --------------- |
| `gh`      | `brew install gh`               | `apt install gh`                | GitHub CLI      |
| `jq`      | `brew install jq`               | `apt install jq`                | JSON processing |
| `aws`     | `brew install awscli`           | `apt install awscli`            | AWS CLI         |
| `gcloud`  | `brew install google-cloud-sdk` | See docs                        | Google Cloud    |
| `kubectl` | `brew install kubectl`          | See docs                        | Kubernetes      |
| `docker`  | Docker Desktop                  | `apt install docker.io`         | Containers      |
| `rg`      | `brew install ripgrep`          | `apt install ripgrep`           | Fast search     |
| `psql`    | `brew install postgresql`       | `apt install postgresql-client` | Postgres        |
