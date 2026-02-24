# praxis-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![skills: 19](https://img.shields.io/badge/skills-19-informational)](skills/)

Curated, production-grade skills for AI coding agents. No magic, no demos — battle-tested workflows built for developers who use AI seriously.

---

## Overview

`praxis-skills` is a collection of custom skills for [Claude Code](https://claude.ai/code) and Claude.ai. Each skill is a self-contained prompt package that extends Claude with a repeatable, opinionated workflow for a specific task domain.

**Philosophy:** Skills in this collection are practical and context-free. They define the _how_, not just the _what_ — covering inputs, outputs, edge cases, and failure modes. They are tested in real workloads, not constructed as examples.

Intended for developers who treat AI coding agents as a serious part of their workflow.

---

## Skill Catalog

### Development & Tooling

| Skill                                  | Description                                                                                                                                |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| [agent-builder](skills/agent-builder/) | Build AI agents using the Claude Agent SDK and headless CLI mode — covers tool definitions, MCP servers, and programmatic orchestration    |
| [github](skills/github/)               | GitHub CLI operations via `gh` — issues, PRs, CI/Actions, releases, search, REST/GraphQL API, with error handling and automation workflows |
| [mcp-to-skill](skills/mcp-to-skill/)   | Convert MCP servers into on-demand skills to reduce active context window token usage                                                      |
| [gpu-optimizer](skills/gpu-optimizer/) | GPU optimization for consumer GPUs (8-24GB VRAM) — PyTorch, XGBoost, CuPy/RAPIDS, memory management, and CUDA tuning                       |
| [tavily](skills/tavily/)               | AI-optimized web search and content extraction via Tavily API with structured output parsing                                               |

### Review & Quality

| Skill                                                  | Description                                                                                                                                        |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [architecture-reviewer](skills/architecture-reviewer/) | Architecture reviews across 7 scored dimensions — structural integrity, scalability, security, performance, enterprise readiness, operations, data |
| [manuscript-review](skills/manuscript-review/)         | Pre-publication manuscript audit with 24 diagnostic dimensions, citation hygiene, and cross-element coherence                                      |
| [manuscript-provenance](skills/manuscript-provenance/) | Computational provenance audit verifying every number, table, and figure in a manuscript traces back to code                                       |
| [repo-sentinel](skills/repo-sentinel/)                 | Security audit and enforcement for public repos — 12 attack surfaces, pre-release readiness, history scrubbing, CI gates                           |
| [skill-evaluator](skills/skill-evaluator/)             | Evaluate skill quality across 6 weighted dimensions — frontmatter, triggers, structure, depth, consistency, compliance                             |

### Visualization & Documents

| Skill                                                                | Description                                                                                                      |
| -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| [architecture-diagram](skills/architecture-diagram/)                 | Layered architecture diagrams as self-contained HTML with inline SVG icons and CSS Grid layout                   |
| [concept-to-image](skills/concept-to-image/)                         | Turn concepts into polished HTML visuals, export as PNG or SVG                                                   |
| [concept-to-video](skills/concept-to-video/)                         | Turn concepts into animated explainer videos using Manim — MP4/GIF output with iterative preview                 |
| [html-presentation](skills/html-presentation/)                       | Convert documents and outlines into self-contained HTML slide presentations                                      |
| [static-web-artifacts-builder](skills/static-web-artifacts-builder/) | Self-contained interactive HTML artifacts — infographics, dashboards, diagrams                                   |
| [md-to-pdf](skills/md-to-pdf/)                                       | Markdown to styled PDF with Mermaid diagrams, KaTeX math, and syntax highlighting                                |
| [doc-condenser](skills/doc-condenser/)                               | Transform verbose technical documentation into concise, scannable specs with KEEP/CONDENSE/REMOVE classification |

### Writing & Reasoning

| Skill                                              | Description                                                                                         |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [linkedin-post-style](skills/linkedin-post-style/) | Write LinkedIn posts matching a specific technical author's voice — direct, analytical, dry-humored |
| [sequential-thinking](skills/sequential-thinking/) | Structured chain-of-thought reasoning with revision, branching, and scope tracking                  |

---

## Installation

**Option 1 — Skills CLI (recommended)**

Install any skill directly using [`npx skills`](https://github.com/vercel-labs/skills):

```bash
# Install all skills
npx skills add Mathews-Tom/praxis-skills

# Install a specific skill
npx skills add Mathews-Tom/praxis-skills -s architecture-reviewer

# List available skills without installing
npx skills add Mathews-Tom/praxis-skills -l
```

**Option 2 — TUI Installer**

```bash
git clone https://github.com/Mathews-Tom/praxis-skills.git
cd praxis-skills
uv run scripts/install_skills.py
```

Displays a version-aware table of all skills, detects installed versions, and lets you select which to install or upgrade.

**Option 3 — Manual**

Clone the repo and point Claude Code at individual skill folders:

```bash
git clone https://github.com/Mathews-Tom/praxis-skills.git
claude --add-dir praxis-skills/skills/architecture-reviewer
```

Or download `.skill` archives from the [Releases](../../releases) page.

---

## Usage

Skills activate when Claude detects a matching intent in your message. Each skill defines trigger phrases in its frontmatter description — check the `SKILL.md` in each folder for the full list.

**Example triggers:**

```
"Create an architecture diagram for my microservices setup"
→ activates: architecture-diagram

"Run a security audit before I push this to GitHub"
→ activates: repo-sentinel

"Convert this markdown file to PDF with the Mermaid diagrams rendered"
→ activates: md-to-pdf

"Build an agent that monitors a directory for changes"
→ activates: agent-builder

"Evaluate the quality of this skill"
→ activates: skill-evaluator
```

Skills do not require explicit invocation — Claude matches your intent against the skill's trigger definition and loads it automatically when relevant.

---

## Skill Quality

Every skill in this repo is evaluated against 6 dimensions using the [skill-evaluator](skills/skill-evaluator/):

| Dimension               | Weight | What it measures                                            |
| ----------------------- | ------ | ----------------------------------------------------------- |
| Frontmatter Quality     | 20%    | Description length, trigger phrases, "Use when" clause      |
| Trigger Coverage        | 18%    | Synonym breadth, implied contexts, interrogative forms      |
| Structural Completeness | 20%    | Workflow, error handling, output format, limitations        |
| Content Depth           | 22%    | Decision frameworks, multi-step workflows, output templates |
| Consistency & Integrity | 12%    | Name matching, file references, description-body alignment  |
| CONTRIBUTING Compliance | 8%     | Naming conventions, length limits, YAML validity            |

Run a full audit:

```bash
claude --add-dir skills/skill-evaluator
# Then: "Run a full skill audit on this repo"
```

---

## Packaging

Each skill can be packaged into a `.skill` archive for distribution:

```bash
uv run scripts/package_skill.py skills/architecture-reviewer
```

---

## Portability

These skills are Claude-native (Claude Code and Claude.ai).

Adapters for other agent surfaces are planned in `adapters/`:

- **Cursor** — `.cursorrules`
- **OpenAI Codex** — `AGENTS.md`
- **Gemini CLI** — `GEMINI.md`

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting new skills or improving existing ones.

---

## License

MIT. See [LICENSE](LICENSE) for details.

---

<sub>#AIPraxisPulse</sub>
