# Codebase Signals Guide

Reference for Mode A (Codebase Review) and Mode C (Hybrid). Details what files to locate,
patterns to grep for, and red flags to detect — language-agnostic.

## Table of Contents

1. Priority File Locations
2. Red Flag Patterns to Search For
3. Structural Analysis Approach
4. Per-Dimension Codebase Signals

---

## 1. Priority File Locations

Locate and inspect these categories of files first. The scan_codebase.sh script will identify
most of these, but verify manually for anything missed.

### Infrastructure & Deployment

- `Dockerfile`, `docker-compose.yml` / `docker-compose.yaml`
- `kubernetes/`, `k8s/`, `deploy/`, `infra/` directories
- `*.tf`, `*.tfvars` (Terraform)
- `template.yaml`, `serverless.yml` (SAM / Serverless Framework)
- `pulumi/`, `cdk/` directories
- `nginx.conf`, `caddy`, `traefik.yml` (Reverse proxy configs)
- `Procfile`, `app.yaml`, `render.yaml` (PaaS configs)

### CI/CD Pipeline

- `.github/workflows/*.yml` (GitHub Actions)
- `Jenkinsfile`, `.gitlab-ci.yml`, `buildspec.yml` (Jenkins, GitLab, CodeBuild)
- `bitbucket-pipelines.yml`, `.circleci/config.yml`
- `.pre-commit-config.yaml`

### Dependency Manifests

- `package.json` + `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` (Node.js)
- `requirements.txt` / `pyproject.toml` / `Pipfile` / `poetry.lock` (Python)
- `go.mod` + `go.sum` (Go)
- `Cargo.toml` + `Cargo.lock` (Rust)
- `pom.xml` / `build.gradle` / `build.gradle.kts` (Java/Kotlin)
- `Gemfile` + `Gemfile.lock` (Ruby)
- `composer.json` + `composer.lock` (PHP)

### API Definitions

- `openapi.yaml` / `swagger.json` / `*.openapi.yml`
- `schema.graphql` / `*.graphql`
- `*.proto` (Protocol Buffers / gRPC)
- Route definition files (framework-specific)

### Database & Data

- `migrations/`, `db/migrate/`, `alembic/` directories
- Schema definition files (ORM models, SQL DDL files)
- Seed files, fixtures
- `.env`, `.env.example`, `.env.local`

### Testing

- `tests/`, `test/`, `__tests__/`, `spec/` directories
- Test configuration (jest.config.js, pytest.ini, phpunit.xml)
- `.codecov.yml`, `.coveragerc`

### Documentation

- `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`
- `adr/`, `docs/`, `wiki/` directories
- `CHANGELOG.md`, `SECURITY.md`

---

## 2. Red Flag Patterns to Search For

### Security Red Flags (CRITICAL — always check)

```text
# Hardcoded secrets (search recursively, exclude lock files and node_modules)
password\s*=\s*["\']
api_key\s*=\s*["\']
secret\s*=\s*["\']
token\s*=\s*["\']
AWS_ACCESS_KEY
PRIVATE.KEY
-----BEGIN RSA PRIVATE KEY-----
-----BEGIN OPENSSH PRIVATE KEY-----

# SQL injection vectors
"SELECT.*\+.*"       # String concatenation in queries
f"SELECT              # f-string SQL (Python)
`SELECT.*\$\{`        # Template literal SQL (JavaScript)
".*" \+ .*WHERE       # Concatenated WHERE clauses

# Debug/dev in production
DEBUG\s*=\s*[Tt]rue
NODE_ENV\s*=\s*development  (in non-.env files)
```

### Architecture Red Flags

```text
# In-memory state (prevents horizontal scaling)
session_store.*memory
InMemoryCache
new Map().*session   # Session stored in local Map
global.*state        # Global mutable state

# Missing error handling
catch.*\{\s*\}       # Empty catch blocks
\.catch\(\)          # Empty promise catch
except:\s*pass       # Python bare except pass

# Tight coupling indicators
import.*from.*\.\.\/\.\.\/  # Deep relative imports
require\(.*\.\.\/\.\.\/     # Deep relative requires (Node.js)
```

### Performance Red Flags

```text
# N+1 query patterns
for.*\{.*\.find\(    # Query inside loop
for.*\{.*\.get\(     # DB get inside loop
for.*\{.*SELECT      # SQL inside loop
\.map\(.*await       # Async query in map without Promise.all

# Missing pagination
findAll\(\)          # Unbounded queries
SELECT.*FROM.*(?!.*LIMIT)  # SELECT without LIMIT
.find\(\{\}\)        # MongoDB find-all
```

---

## 3. Structural Analysis Approach

After the scan script runs, perform this manual analysis:

### Step 1: Map Service Boundaries

- Identify top-level directories or separate packages/modules
- For monorepos: identify service directories
- Map the dependency graph between services/modules
- Check for shared libraries and their scope

### Step 2: Identify the Critical Path

- Trace the primary user flow from entry point to response
- Count the number of network hops, database queries, and external calls
- Identify synchronous chains that could be parallelized or made async

### Step 3: Assess Configuration Hygiene

- Check .gitignore for .env exclusion
- Verify no secrets in committed configuration files
- Check for environment-specific configuration patterns
- Look for hardcoded URLs, ports, or environment-specific values

### Step 4: Evaluate Test Coverage Indicators

- Ratio of test files to source files
- Presence of integration and E2E tests (not just unit tests)
- Test configuration indicating coverage thresholds
- CI pipeline test execution steps

---

## 4. Per-Dimension Codebase Signals

Quick reference for what to inspect per dimension:

| Dimension              | Key Files to Inspect                                                    | Key Patterns to Search                                                           |
| ---------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Structural Integrity   | Module boundaries, interfaces, import graphs                            | Circular imports, god classes (files >500 LOC), shared DB schemas                |
| Scalability            | Session stores, cache configs, queue configs, auto-scaling rules        | In-memory state, local file deps, connection pool settings                       |
| Enterprise Readiness   | Auth middleware, tenant ID propagation, audit logging, RBAC policies    | Tenant scoping in queries, compliance-related code, deployment configs           |
| Performance            | ORM queries, cache implementations, async patterns, connection pools    | N+1 queries, unbounded selects, synchronous external calls in hot path           |
| Security               | Auth/authz middleware, input validation, CORS config, secret references | Hardcoded secrets, SQL concatenation, overly permissive CORS, missing validation |
| Operational Excellence | CI/CD configs, IaC files, logging code, health endpoints, metrics       | Unstructured logs, missing health checks, no tracing instrumentation             |
| Data Architecture      | Migration files, schema definitions, event schemas, backup configs      | Missing constraints, no migration tool, no index definitions                     |
