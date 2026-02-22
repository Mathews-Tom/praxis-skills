# Templates Reference

Ready-to-use configurations for automated enforcement, .gitignore generation, and CI gates.

---

## Pre-Commit Configuration

Drop this `.pre-commit-config.yaml` into the repo root. Requires `pip install pre-commit`
then `pre-commit install`.

```yaml
repos:
  # Detect secrets before they reach the repo
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4  # Pin to specific version
    hooks:
      - id: gitleaks

  # Yelp's detect-secrets (complementary entropy-based detection)
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  # Prevent large files from being committed
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: detect-private-key
      - id: check-merge-conflict
      - id: no-commit-to-branch
        args: ['--branch', 'main', '--branch', 'master']

  # Block .env files (non-example)
  - repo: local
    hooks:
      - id: block-env-files
        name: Block .env files
        entry: bash -c 'git diff --cached --name-only | grep -iE "\.env(\.|$)" | grep -v "\.example$\|\.template$" && echo "ERROR: .env file staged" && exit 1 || exit 0'
        language: system
        pass_filenames: false

      # Block .claude/ and CLAUDE.md
      - id: block-claude-files
        name: Block .claude/ and CLAUDE.md
        entry: bash -c 'git diff --cached --name-only | grep -iE "(\.claude/|claude\.md)" && echo "ERROR: .claude/ or CLAUDE.md staged" && exit 1 || exit 0'
        language: system
        pass_filenames: false

      # Block credential files
      - id: block-credential-files
        name: Block credential files
        entry: bash -c 'git diff --cached --name-only | grep -iE "\.(pem|key|p12|pfx|credentials|keystore|jks|tfstate)$" && echo "ERROR: Credential file staged" && exit 1 || exit 0'
        language: system
        pass_filenames: false
```

### Initial setup commands

```bash
pip install pre-commit
pre-commit install

# Create detect-secrets baseline (marks existing known strings)
detect-secrets scan > .secrets.baseline

# Verify hooks work
pre-commit run --all-files
```

---

## GitHub Actions — Secret Scanning CI Gate

Add as `.github/workflows/repo-sentinel.yml`:

```yaml
name: Repo Sentinel

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

permissions:
  contents: read
  security-events: write

jobs:
  secret-scan:
    name: Secret Detection
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2 — pinned to SHA
        with:
          fetch-depth: 0 # Full history for history scan

      - name: Gitleaks scan
        uses: gitleaks/gitleaks-action@cb7149a9b57195b609c63e8518d2c6056677d2d0 # v2.3.7
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  env-file-check:
    name: .env File Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - name: Check for tracked .env files
        run: |
          FOUND=$(git ls-files | grep -iE '\.env(\.|$)' | grep -v '\.example$\|\.template$' || true)
          if [ -n "$FOUND" ]; then
            echo "::error::Tracked .env files found:"
            echo "$FOUND"
            exit 1
          fi

  claude-files-check:
    name: Claude Files Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - name: Check for .claude/ and CLAUDE.md
        run: |
          FOUND=$(git ls-files | grep -iE '(\.claude/|claude\.md)' || true)
          if [ -n "$FOUND" ]; then
            echo "::error::Claude files tracked:"
            echo "$FOUND"
            exit 1
          fi

  credential-file-check:
    name: Credential File Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - name: Check for credential files
        run: |
          FOUND=$(git ls-files | grep -iE '\.(pem|key|p12|pfx|credentials|keystore|jks|tfstate)$' || true)
          if [ -n "$FOUND" ]; then
            echo "::error::Credential files tracked:"
            echo "$FOUND"
            exit 1
          fi

  internal-url-check:
    name: Internal URL Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - name: Check for internal URLs
        run: |
          FOUND=$(git grep -rnE 'https?://[^\s)>"]*\.(internal|corp|local|intranet|private)' -- ':!*.lock' ':!node_modules' || true)
          if [ -n "$FOUND" ]; then
            echo "::warning::Internal URLs found:"
            echo "$FOUND"
          fi

  license-check:
    name: License Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - name: Check LICENSE exists
        run: |
          if ! ls LICENSE* LICENCE* 2>/dev/null | head -1 > /dev/null; then
            echo "::warning::No LICENSE file found"
          fi
```

---

## .gitignore Generator

Generate a complete .gitignore based on detected project type. All hygiene rules are built in.

### Universal block (always include)

```gitignore
.env
.env.*
!.env.example
!.env.template
.claude/
CLAUDE.md
*.pem
*.key
*.p12
*.pfx
*.credentials
*.credentials.json
*.keystore
*.jks
*.tfstate
*.tfstate.backup
*.tfvars
!*.tfvars.example
.secrets.baseline
```

### Python projects (add to universal)

```gitignore
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
*.egg
.venv/
venv/
.pytest_cache/
.mypy_cache/
.ruff_cache/
htmlcov/
.coverage
*.sqlite3
*.db
```

### Node.js projects (add to universal)

```gitignore
node_modules/
.npm/
dist/
build/
*.tgz
.next/
.nuxt/
.cache/
coverage/
.nyc_output/
.npmrc
```

### Go projects (add to universal)

```gitignore
vendor/
*.exe
*.dll
*.so
*.dylib
*.test
*.out
```

### Rust projects (add to universal)

```gitignore
target/
Cargo.lock
```

### Editor/IDE (always include)

```gitignore
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db
```

### Generation logic

When generating .gitignore:

1. Start with universal block
2. Detect project type from files present (package.json → Node, pyproject.toml/setup.py → Python, go.mod → Go, Cargo.toml → Rust)
3. Append language-specific block
4. Always append editor/IDE block
5. Zero comments in output
6. Verify no redundant entries (directory pattern absorbs children)
7. Run `git ls-files -i --exclude-standard` to check for contradictions

---

## SECURITY.md Template

```markdown
# Security Policy

## Supported Versions

| Version  | Supported |
| -------- | --------- |
| latest   | ✅        |
| < latest | ❌        |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT open a public issue.**
2. Email: [security@your-domain.com](mailto:security@your-domain.com)
3. Include: description, steps to reproduce, potential impact.
4. You will receive acknowledgment within 48 hours.
5. We will work with you to understand and address the issue before any public disclosure.

## Scope

This policy applies to the latest release of this project. We appreciate your efforts to
responsibly disclose your findings.
```

---

## Issue Template — Bug Report (safe)

Save as `.github/ISSUE_TEMPLATE/bug_report.yml`:

```yaml
name: Bug Report
description: Report a bug
labels: [bug]
body:
  - type: markdown
    attributes:
      value: |
        ⚠️ **DO NOT include any credentials, API keys, tokens, passwords, or connection strings in this report.**
        Sanitize all logs and outputs before pasting.

  - type: textarea
    id: description
    attributes:
      label: Description
      description: What happened?
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to reproduce
      description: Minimal steps to reproduce (use placeholder values for any secrets)
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
    validations:
      required: true

  - type: input
    id: version
    attributes:
      label: Version
      description: Which version are you using?
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Relevant logs
      description: |
        Paste sanitized logs here. Remove any:
        - API keys, tokens, passwords
        - Internal URLs or IP addresses
        - Personal information
      render: shell
```

---

## PR Template (safe)

Save as `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## What

<!-- Brief description of what this PR does -->

## Why

<!-- Why is this change needed? Link to public issue if applicable -->

## How

<!-- How was this implemented? Key design decisions -->

## Checklist

- [ ] No credentials, secrets, or internal URLs in code or comments
- [ ] No .env files (only .env.example with placeholders)
- [ ] No .claude/ or CLAUDE.md files
- [ ] Tests use synthetic/mock data (no real PII)
- [ ] Documentation uses placeholder URLs (example.com)
- [ ] Pre-commit hooks pass locally
```

---

## Scheduled Audit (Weekly CI Job)

Add as `.github/workflows/weekly-audit.yml`:

```yaml
name: Weekly Repo Sentinel Audit

on:
  schedule:
    - cron: "0 9 * * 1" # Every Monday at 9 AM UTC
  workflow_dispatch: # Allow manual trigger

permissions:
  contents: read
  issues: write

jobs:
  weekly-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
        with:
          fetch-depth: 0

      - name: Install gitleaks
        run: |
          wget -q https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_8.18.4_linux_x64.tar.gz
          tar -xzf gitleaks_8.18.4_linux_x64.tar.gz
          sudo mv gitleaks /usr/local/bin/

      - name: Run full audit
        run: |
          echo "=== REPO SENTINEL WEEKLY AUDIT ===" > audit-report.txt
          echo "Date: $(date -u)" >> audit-report.txt
          echo "" >> audit-report.txt

          # Secret scan
          echo "[Secret Scan]" >> audit-report.txt
          gitleaks detect --source . --verbose 2>&1 >> audit-report.txt || true
          echo "" >> audit-report.txt

          # Tracked .env files
          echo "[Tracked .env Files]" >> audit-report.txt
          git ls-files | grep -iE '\.env(\.|$)' | grep -v '\.example$\|\.template$' >> audit-report.txt 2>&1 || echo "None" >> audit-report.txt
          echo "" >> audit-report.txt

          # Credential files
          echo "[Credential Files]" >> audit-report.txt
          git ls-files | grep -iE '\.(pem|key|p12|pfx|credentials|keystore|jks|tfstate)$' >> audit-report.txt 2>&1 || echo "None" >> audit-report.txt
          echo "" >> audit-report.txt

          # Internal URLs
          echo "[Internal URLs]" >> audit-report.txt
          git grep -rnE 'https?://[^\s)>"]*\.(internal|corp|local|intranet|private)' -- ':!*.lock' ':!node_modules' >> audit-report.txt 2>&1 || echo "None" >> audit-report.txt

          cat audit-report.txt

      - name: Check for findings
        run: |
          if grep -qE '(CRITICAL|WARNING|leaks? found|\.env\.|\.pem|\.key)' audit-report.txt; then
            echo "::error::Audit findings detected — review audit-report.txt"
            exit 1
          fi
```
