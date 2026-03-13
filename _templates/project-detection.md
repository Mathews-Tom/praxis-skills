# Project Detection Reference

Stack-agnostic project detection patterns for identifying test commands, package managers, version strategies, frameworks, monorepo configurations, and CI/CD systems.

---

## Test Command Resolution

Detect the project's test command by checking these files in order:

| Check | File | Condition | Command |
|-------|------|-----------|---------|
| 1 | `Makefile` | Has `test:` target | `make test` |
| 2 | `package.json` | Has `scripts.test` | `{pkg-manager} run test` |
| 3 | `pyproject.toml` | Has `[tool.pytest]` or `pytest` dependency | `uv run pytest` (if `uv.lock`), `poetry run pytest` (if `poetry.lock`), `pytest` |
| 4 | `Cargo.toml` | Exists | `cargo test` |
| 5 | `go.mod` | Exists | `go test ./...` |
| 6 | `Gemfile` + `Rakefile` | Has `test` task | `bundle exec rake test` |
| 7 | `mix.exs` | Exists | `mix test` |
| 8 | `build.gradle` / `build.gradle.kts` | Exists | `./gradlew test` |
| 9 | `pom.xml` | Exists | `mvn test` |

If multiple match, prefer the first in order. If `Makefile` exists with a `test` target, it is always authoritative — projects use Makefiles to wrap their actual test commands.

---

## Package Manager Detection

Detect from lock files (most specific wins):

| Lock File | Package Manager | Run Command |
|-----------|----------------|-------------|
| `pnpm-lock.yaml` | pnpm | `pnpm run` |
| `bun.lockb` | bun | `bun run` |
| `yarn.lock` | yarn | `yarn run` |
| `package-lock.json` | npm | `npm run` |
| `uv.lock` | uv | `uv run` |
| `poetry.lock` | poetry | `poetry run` |
| `Pipfile.lock` | pipenv | `pipenv run` |
| `Cargo.lock` | cargo | `cargo` |
| `go.sum` | go modules | `go` |
| `Gemfile.lock` | bundler | `bundle exec` |
| `mix.lock` | mix | `mix` |

If no lock file: fall back to manifest file detection (`package.json` → npm, `pyproject.toml` → check for `[tool.poetry]` or default to uv).

---

## Version Strategy Detection

Check in order:

| Strategy | Detection | Read | Write |
|----------|-----------|------|-------|
| `VERSION` file | File named `VERSION` at repo root | Read contents | Write new version |
| `package.json` | Has `version` field | `jq -r .version package.json` | `jq '.version = "X.Y.Z"' package.json` |
| `pyproject.toml` | Has `[project] version` or `[tool.poetry] version` | Parse TOML | Update TOML |
| `Cargo.toml` | Has `[package] version` | Parse TOML | Update TOML (+ `Cargo.lock`) |
| `mix.exs` | Has `version:` in project config | Regex extract | Regex replace |
| Git tags only | No version file, but `v*` tags exist | `git describe --tags --abbrev=0` | `git tag vX.Y.Z` |

For PATCH bumps: increment automatically. For MINOR or MAJOR: require explicit confirmation.

---

## Framework Detection

Detect by analyzing dependencies and configuration files:

### Python
| Framework | Detection |
|-----------|-----------|
| Django | `django` in dependencies, `manage.py` exists |
| FastAPI | `fastapi` in dependencies |
| Flask | `flask` in dependencies |
| Starlette | `starlette` in dependencies (without FastAPI) |

### JavaScript/TypeScript
| Framework | Detection |
|-----------|-----------|
| Next.js | `next` in dependencies, `next.config.*` exists |
| Remix | `@remix-run/node` in dependencies |
| SvelteKit | `@sveltejs/kit` in dependencies |
| Nuxt | `nuxt` in dependencies |
| Express | `express` in dependencies (without meta-framework) |
| Astro | `astro` in dependencies |
| Vite (library) | `vite` in dependencies (without meta-framework) |

### Ruby
| Framework | Detection |
|-----------|-----------|
| Rails | `rails` in Gemfile, `config/routes.rb` exists |
| Sinatra | `sinatra` in Gemfile |

### Go
| Framework | Detection |
|-----------|-----------|
| Gin | `github.com/gin-gonic/gin` in `go.mod` |
| Echo | `github.com/labstack/echo` in `go.mod` |
| Chi | `github.com/go-chi/chi` in `go.mod` |
| Standard library | No framework dependency |

### Rust
| Framework | Detection |
|-----------|-----------|
| Actix-web | `actix-web` in `Cargo.toml` |
| Axum | `axum` in `Cargo.toml` |
| Rocket | `rocket` in `Cargo.toml` |

### Default Ports by Framework

| Framework | Default Port |
|-----------|-------------|
| Next.js | 3000 |
| Remix | 3000 |
| SvelteKit | 5173 |
| Nuxt | 3000 |
| Vite | 5173 |
| Express | 3000 |
| Django | 8000 |
| FastAPI | 8000 |
| Flask | 5000 |
| Rails | 3000 |
| Phoenix | 4000 |
| Go (common) | 8080 |
| Rust (common) | 8080 |

---

## Monorepo Detection

| Signal | Tool | Configuration |
|--------|------|---------------|
| `pnpm-workspace.yaml` | pnpm workspaces | `packages:` array lists workspace globs |
| `turbo.json` | Turborepo | `pipeline:` defines task dependencies |
| `nx.json` | Nx | `targetDefaults:` defines build graph |
| `lerna.json` | Lerna | `packages:` array lists package locations |
| `[workspace]` in `Cargo.toml` | Cargo workspaces | `members:` array lists crate paths |
| `go.work` | Go workspaces | `use` directives list module paths |
| `settings.gradle` / `settings.gradle.kts` | Gradle multi-project | `include` statements list subprojects |

For monorepos, scope operations to the relevant workspace/package when a path is specified.

---

## CI/CD Detection

| Path | System |
|------|--------|
| `.github/workflows/*.yml` | GitHub Actions |
| `.gitlab-ci.yml` | GitLab CI |
| `Jenkinsfile` | Jenkins |
| `.circleci/config.yml` | CircleCI |
| `bitbucket-pipelines.yml` | Bitbucket Pipelines |
| `.travis.yml` | Travis CI |
| `azure-pipelines.yml` | Azure DevOps |
| `.buildkite/pipeline.yml` | Buildkite |
| `Taskfile.yml` | Task (not CI, but task runner) |

---

## Changelog Detection

| File | Format |
|------|--------|
| `CHANGELOG.md` | Keep a Changelog (most common) |
| `CHANGES.md` | Variant naming |
| `HISTORY.md` | Variant naming |
| `NEWS.md` | GNU-style |
| None | Skip changelog updates |

Keep a Changelog format:
```markdown
## [X.Y.Z] - YYYY-MM-DD
### Added
### Changed
### Fixed
### Removed
```
