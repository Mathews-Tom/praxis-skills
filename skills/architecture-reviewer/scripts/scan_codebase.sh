#!/usr/bin/env bash
# scan_codebase.sh — Produce a structural fingerprint of a codebase for architecture review.
# Usage: bash scan_codebase.sh <path_to_codebase>
# Output: Structured summary to stdout

set -euo pipefail

CODEBASE="${1:-.}"

if [ ! -d "$CODEBASE" ]; then
    echo "ERROR: Directory '$CODEBASE' does not exist."
    exit 1
fi

cd "$CODEBASE"

echo "=============================================="
echo "ARCHITECTURE REVIEW — CODEBASE SCAN"
echo "=============================================="
echo "Scanned path: $(pwd)"
echo "Scan date:    $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# ── 1. Project Overview ──────────────────────────────────────────────────────

echo "══════════════════════════════════════════════"
echo "1. PROJECT OVERVIEW"
echo "══════════════════════════════════════════════"

# Total file count (excluding .git, node_modules, vendor, __pycache__, .venv)
FILE_COUNT=$(find . \
    -not -path './.git/*' \
    -not -path '*/node_modules/*' \
    -not -path '*/vendor/*' \
    -not -path '*/__pycache__/*' \
    -not -path '*/.venv/*' \
    -not -path '*/.env/*' \
    -not -path '*/dist/*' \
    -not -path '*/build/*' \
    -not -path '*/.next/*' \
    -type f 2>/dev/null | wc -l | tr -d ' ')
echo "Total files (excluding generated): $FILE_COUNT"

# LOC estimate (source files only)
LOC_ESTIMATE=$(find . \
    -not -path './.git/*' \
    -not -path '*/node_modules/*' \
    -not -path '*/vendor/*' \
    -not -path '*/__pycache__/*' \
    -not -path '*/.venv/*' \
    -not -path '*/dist/*' \
    -not -path '*/build/*' \
    -not -path '*/.next/*' \
    \( -name '*.py' -o -name '*.js' -o -name '*.ts' -o -name '*.tsx' -o -name '*.jsx' \
       -o -name '*.go' -o -name '*.rs' -o -name '*.java' -o -name '*.kt' -o -name '*.rb' \
       -o -name '*.php' -o -name '*.cs' -o -name '*.cpp' -o -name '*.c' -o -name '*.swift' \
       -o -name '*.scala' -o -name '*.ex' -o -name '*.exs' -o -name '*.zig' \
       -o -name '*.vue' -o -name '*.svelte' -o -name '*.dart' \) \
    -type f -exec cat {} + 2>/dev/null | wc -l | tr -d ' ')
echo "Estimated source LOC: $LOC_ESTIMATE"

# Primary languages
echo ""
echo "Language distribution (by file count):"
find . \
    -not -path './.git/*' \
    -not -path '*/node_modules/*' \
    -not -path '*/vendor/*' \
    -not -path '*/__pycache__/*' \
    -not -path '*/.venv/*' \
    -not -path '*/dist/*' \
    -not -path '*/build/*' \
    \( -name '*.py' -o -name '*.js' -o -name '*.ts' -o -name '*.tsx' -o -name '*.jsx' \
       -o -name '*.go' -o -name '*.rs' -o -name '*.java' -o -name '*.kt' -o -name '*.rb' \
       -o -name '*.php' -o -name '*.cs' -o -name '*.cpp' -o -name '*.c' -o -name '*.swift' \
       -o -name '*.scala' -o -name '*.ex' -o -name '*.exs' -o -name '*.vue' -o -name '*.svelte' \
       -o -name '*.dart' -o -name '*.zig' \) \
    -type f 2>/dev/null | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10 || true

# Git info
echo ""
if [ -d .git ]; then
    FIRST_COMMIT=$(git log --reverse --format='%ai' 2>/dev/null | head -1 || echo "unknown")
    LAST_COMMIT=$(git log -1 --format='%ai' 2>/dev/null || echo "unknown")
    COMMIT_COUNT=$(git rev-list --count HEAD 2>/dev/null || echo "unknown")
    CONTRIBUTOR_COUNT=$(git log --format='%ae' 2>/dev/null | sort -u | wc -l | tr -d ' ' || echo "unknown")
    echo "Git repository: YES"
    echo "  First commit:   $FIRST_COMMIT"
    echo "  Last commit:    $LAST_COMMIT"
    echo "  Total commits:  $COMMIT_COUNT"
    echo "  Contributors:   $CONTRIBUTOR_COUNT"
else
    echo "Git repository: NO"
fi

# ── 2. Architecture Indicators ───────────────────────────────────────────────

echo ""
echo "══════════════════════════════════════════════"
echo "2. ARCHITECTURE INDICATORS"
echo "══════════════════════════════════════════════"

echo ""
echo "Directory tree (top 2 levels):"
find . -maxdepth 2 -type d \
    -not -path './.git*' \
    -not -path '*/node_modules*' \
    -not -path '*/vendor*' \
    -not -path '*/__pycache__*' \
    -not -path '*/.venv*' \
    -not -path '*/dist*' \
    -not -path '*/build*' \
    -not -path '*/.next*' \
    2>/dev/null | head -50 | sed 's/[^/]*/│  /g;s/│  \([^│]\)/├── \1/' || true

# Monorepo detection
echo ""
WORKSPACE_FILES=$(find . -maxdepth 2 \( -name 'pnpm-workspace.yaml' -o -name 'lerna.json' \
    -o -name 'nx.json' -o -name 'turbo.json' -o -name 'rush.json' \) 2>/dev/null || true)
if [ -n "$WORKSPACE_FILES" ]; then
    echo "Monorepo indicator: YES"
    echo "  $WORKSPACE_FILES"
else
    echo "Monorepo indicator: NO (or not detected)"
fi

# ── 3. Infrastructure Files ──────────────────────────────────────────────────

echo ""
echo "══════════════════════════════════════════════"
echo "3. INFRASTRUCTURE FILES"
echo "══════════════════════════════════════════════"

echo ""
echo "Docker:"
find . -maxdepth 4 \( -name 'Dockerfile*' -o -name 'docker-compose*.yml' -o -name 'docker-compose*.yaml' \
    -o -name '.dockerignore' \) -not -path '*/node_modules/*' 2>/dev/null | head -20 || echo "  (none found)"

echo ""
echo "Kubernetes:"
find . -maxdepth 4 \( -name '*.yaml' -o -name '*.yml' \) -not -path '*/node_modules/*' \
    -not -path './.git/*' -exec grep -l 'apiVersion:' {} \; 2>/dev/null | head -20 || echo "  (none found)"

echo ""
echo "Terraform / IaC:"
find . -maxdepth 4 \( -name '*.tf' -o -name '*.tfvars' -o -name 'template.yaml' \
    -o -name 'serverless.yml' -o -name 'serverless.yaml' -o -name 'cdk.json' \
    -o -name 'Pulumi.yaml' \) -not -path '*/node_modules/*' 2>/dev/null | head -20 || echo "  (none found)"

echo ""
echo "Reverse Proxy / Load Balancer:"
find . -maxdepth 4 \( -name 'nginx*.conf' -o -name 'Caddyfile' -o -name 'traefik*.yml' \
    -o -name 'traefik*.yaml' -o -name 'haproxy*.cfg' \) -not -path '*/node_modules/*' \
    2>/dev/null | head -10 || echo "  (none found)"

echo ""
echo "CI/CD:"
find . -maxdepth 3 \( -name '*.yml' -o -name '*.yaml' \) -path '*/.github/workflows/*' 2>/dev/null || true
find . -maxdepth 2 \( -name 'Jenkinsfile' -o -name '.gitlab-ci.yml' -o -name 'buildspec.yml' \
    -o -name 'bitbucket-pipelines.yml' -o -name '.circleci' \) 2>/dev/null || true
[ -z "$(find . -maxdepth 3 \( -path '*/.github/workflows/*' -o -name 'Jenkinsfile' \
    -o -name '.gitlab-ci.yml' -o -name 'buildspec.yml' \) 2>/dev/null)" ] && echo "  (none found)" || true

# ── 4. Dependency Health ─────────────────────────────────────────────────────

echo ""
echo "══════════════════════════════════════════════"
echo "4. DEPENDENCY HEALTH"
echo "══════════════════════════════════════════════"

echo ""
echo "Dependency manifests found:"
find . -maxdepth 3 \( \
    -name 'package.json' -o -name 'requirements.txt' -o -name 'pyproject.toml' \
    -o -name 'Pipfile' -o -name 'go.mod' -o -name 'Cargo.toml' \
    -o -name 'pom.xml' -o -name 'build.gradle' -o -name 'build.gradle.kts' \
    -o -name 'Gemfile' -o -name 'composer.json' -o -name 'mix.exs' \
    -o -name 'pubspec.yaml' -o -name 'Package.swift' \
    \) -not -path '*/node_modules/*' -not -path '*/vendor/*' 2>/dev/null || echo "  (none found)"

echo ""
echo "Lock files found:"
find . -maxdepth 3 \( \
    -name 'package-lock.json' -o -name 'yarn.lock' -o -name 'pnpm-lock.yaml' \
    -o -name 'poetry.lock' -o -name 'Pipfile.lock' -o -name 'go.sum' \
    -o -name 'Cargo.lock' -o -name 'Gemfile.lock' -o -name 'composer.lock' \
    -o -name 'mix.lock' -o -name 'pubspec.lock' -o -name 'Package.resolved' \
    \) -not -path '*/node_modules/*' -not -path '*/vendor/*' 2>/dev/null || echo "  (none found)"

echo ""
echo "Environment files:"
find . -maxdepth 3 \( -name '.env' -o -name '.env.*' -o -name 'env.*' \) \
    -not -path '*/node_modules/*' -not -path './.git/*' 2>/dev/null || echo "  (none found)"

# Check if .env is in .gitignore
if [ -f .gitignore ]; then
    if grep -q '\.env' .gitignore 2>/dev/null; then
        echo "  .env in .gitignore: YES ✓"
    else
        echo "  .env in .gitignore: NO ✗ (SECURITY CONCERN)"
    fi
fi

# ── 5. API Surface ───────────────────────────────────────────────────────────

echo ""
echo "══════════════════════════════════════════════"
echo "5. API SURFACE"
echo "══════════════════════════════════════════════"

echo ""
echo "API definition files:"
find . -maxdepth 4 \( \
    -name 'openapi.*' -o -name 'swagger.*' -o -name '*.openapi.yml' -o -name '*.openapi.yaml' \
    -o -name 'schema.graphql' -o -name '*.graphql' -o -name '*.gql' \
    -o -name '*.proto' \
    \) -not -path '*/node_modules/*' -not -path '*/vendor/*' 2>/dev/null | head -20 || echo "  (none found)"

# ── 6. Testing Indicators ────────────────────────────────────────────────────

echo ""
echo "══════════════════════════════════════════════"
echo "6. TESTING INDICATORS"
echo "══════════════════════════════════════════════"

echo ""
echo "Test directories:"
find . -maxdepth 3 -type d \( \
    -name 'tests' -o -name 'test' -o -name '__tests__' -o -name 'spec' \
    -o -name 'e2e' -o -name 'integration' -o -name 'unit' \
    \) -not -path '*/node_modules/*' -not -path '*/vendor/*' 2>/dev/null | head -20 || echo "  (none found)"

# Test file count
TEST_FILES=$(find . \( -name '*test*' -o -name '*spec*' -o -name '*_test.*' -o -name '*.test.*' \
    -o -name '*.spec.*' \) -type f \
    -not -path '*/node_modules/*' -not -path '*/vendor/*' -not -path './.git/*' \
    -not -path '*/dist/*' -not -path '*/build/*' 2>/dev/null | wc -l | tr -d ' ')
echo "Test files found: $TEST_FILES"

# Source file count for ratio
SRC_FILES=$(find . \
    -not -path './.git/*' -not -path '*/node_modules/*' -not -path '*/vendor/*' \
    -not -path '*/dist/*' -not -path '*/build/*' -not -path '*/.venv/*' \
    \( -name '*.py' -o -name '*.js' -o -name '*.ts' -o -name '*.tsx' -o -name '*.jsx' \
       -o -name '*.go' -o -name '*.rs' -o -name '*.java' -o -name '*.rb' -o -name '*.php' \) \
    -type f 2>/dev/null | wc -l | tr -d ' ')
if [ "$SRC_FILES" -gt 0 ]; then
    RATIO=$(echo "scale=2; $TEST_FILES / $SRC_FILES * 100" | bc 2>/dev/null || echo "N/A")
    echo "Test-to-source ratio: ${RATIO}% ($TEST_FILES test files / $SRC_FILES source files)"
fi

echo ""
echo "Test config files:"
find . -maxdepth 3 \( \
    -name 'jest.config.*' -o -name 'vitest.config.*' -o -name 'pytest.ini' \
    -o -name 'pyproject.toml' -o -name '.coveragerc' -o -name 'phpunit.xml' \
    -o -name 'karma.conf.*' -o -name 'cypress.config.*' -o -name 'playwright.config.*' \
    -o -name '.codecov.yml' -o -name 'codecov.yml' \
    \) -not -path '*/node_modules/*' 2>/dev/null | head -10 || echo "  (none found)"

# ── 7. Security Indicators ───────────────────────────────────────────────────

echo ""
echo "══════════════════════════════════════════════"
echo "7. SECURITY INDICATORS"
echo "══════════════════════════════════════════════"

echo ""
echo "Security config files:"
find . -maxdepth 3 \( \
    -name '.pre-commit-config.yaml' -o -name '.snyk' -o -name '.trivyignore' \
    -o -name 'SECURITY.md' -o -name '.gitleaks.toml' -o -name '.secretlintrc*' \
    \) -not -path '*/node_modules/*' 2>/dev/null | head -10 || echo "  (none found)"

# Quick secret scan (patterns only, not values)
echo ""
echo "Potential hardcoded secret patterns (file count, not values):"
POTENTIAL_SECRETS=$(grep -rl --include='*.py' --include='*.js' --include='*.ts' --include='*.java' \
    --include='*.go' --include='*.rb' --include='*.php' --include='*.yaml' --include='*.yml' \
    --include='*.json' --include='*.toml' --include='*.cfg' --include='*.ini' \
    -E '(password|api_key|secret_key|access_key|private_key)\s*[=:]\s*["\x27][^\s]+' \
    --exclude-dir=node_modules --exclude-dir=vendor --exclude-dir=.git \
    --exclude-dir=dist --exclude-dir=build --exclude-dir=.venv \
    --exclude='*.lock' --exclude='*.min.js' \
    . 2>/dev/null | wc -l | tr -d ' ')
if [ "$POTENTIAL_SECRETS" -gt 0 ]; then
    echo "  ⚠ Found $POTENTIAL_SECRETS files with potential hardcoded secret patterns"
    echo "    (Manual review recommended — may include false positives from examples/docs)"
else
    echo "  No obvious hardcoded secret patterns detected ✓"
fi

# ── 8. Documentation ─────────────────────────────────────────────────────────

echo ""
echo "══════════════════════════════════════════════"
echo "8. DOCUMENTATION"
echo "══════════════════════════════════════════════"

echo ""
if [ -f README.md ]; then
    README_LOC=$(wc -l < README.md | tr -d ' ')
    echo "README.md: YES ($README_LOC lines)"
else
    echo "README.md: NO"
fi

echo ""
echo "Documentation files:"
find . -maxdepth 3 \( \
    -name 'ARCHITECTURE.md' -o -name 'CONTRIBUTING.md' -o -name 'CHANGELOG.md' \
    -o -name 'DESIGN.md' -o -name 'DEPLOYMENT.md' -o -name 'RUNBOOK.md' \
    \) -not -path '*/node_modules/*' 2>/dev/null || echo "  (none found)"

echo ""
echo "ADR directory:"
find . -maxdepth 3 -type d -name 'adr' -o -name 'ADR' -o -name 'decisions' \
    2>/dev/null || echo "  (none found)"

echo ""
echo "Docs directory:"
find . -maxdepth 2 -type d \( -name 'docs' -o -name 'doc' -o -name 'documentation' \) \
    2>/dev/null || echo "  (none found)"

# ── 9. Largest Files (complexity indicators) ─────────────────────────────────

echo ""
echo "══════════════════════════════════════════════"
echo "9. LARGEST SOURCE FILES (potential god objects)"
echo "══════════════════════════════════════════════"

echo ""
find . \
    -not -path './.git/*' -not -path '*/node_modules/*' -not -path '*/vendor/*' \
    -not -path '*/dist/*' -not -path '*/build/*' -not -path '*/.venv/*' \
    -not -name '*.lock' -not -name '*.min.js' -not -name '*.min.css' \
    -not -name '*.map' -not -name '*.svg' \
    \( -name '*.py' -o -name '*.js' -o -name '*.ts' -o -name '*.tsx' -o -name '*.jsx' \
       -o -name '*.go' -o -name '*.rs' -o -name '*.java' -o -name '*.rb' -o -name '*.php' \) \
    -type f -exec wc -l {} + 2>/dev/null | sort -rn | head -15 || echo "  (could not compute)"

echo ""
echo "=============================================="
echo "SCAN COMPLETE"
echo "=============================================="
