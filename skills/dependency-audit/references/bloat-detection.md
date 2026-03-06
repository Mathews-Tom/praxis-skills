# Bloat Detection

Identifying unused dependencies, duplicate functionality, heavy transitive trees,
and oversized packages in a project's dependency graph.

---

## Unused Dependency Detection

### Strategy

A dependency is unused if no source file in the project imports or references it.

1. **Parse dependency declarations** — Extract all declared dependencies from the manifest
   (`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`).
2. **Scan source files for imports** — Search all source files for import statements
   referencing each dependency.
3. **Flag unmatched** — Dependencies with zero import matches are candidates for removal.

### Language-Specific Import Scanning

#### Python

```python
# Import patterns to search for:
import {package}
from {package} import ...
from {package}.submodule import ...
__import__('{package}')
importlib.import_module('{package}')
```

**Gotcha:** Python package names don't always match import names:
| Package (pip) | Import Name |
|--------------|-------------|
| Pillow | PIL |
| scikit-learn | sklearn |
| python-dateutil | dateutil |
| beautifulsoup4 | bs4 |
| PyYAML | yaml |
| python-dotenv | dotenv |
| opencv-python | cv2 |

Tools:

- `deptry` — Finds unused, missing, and transitive dependencies
- Manual: `uv run deptry .`

#### Node.js

```javascript
// Import patterns to search for:
import ... from '{package}'
import '{package}'
require('{package}')
require('{package}/subpath')
// Dynamic imports
import('{package}')
```

**Gotcha:** Some packages are used via:

- CLI only (build tools like `webpack`, `eslint`) — check `scripts` in `package.json`
- Configuration (plugins referenced in config files) — check `.eslintrc`, `babel.config`, etc.
- Types only (`@types/*`) — check `.d.ts` imports

Tools:

- `depcheck` — `npx depcheck`
- `knip` — `npx knip` (also finds unused exports and files)

#### Rust

```rust
// Import patterns:
use {crate_name}::...
extern crate {crate_name};
// Procedural macros
#[derive({MacroFromCrate})]
```

Tools:

- `cargo-udeps` — `cargo +nightly udeps`
- `cargo-machete` — `cargo machete` (faster, heuristic-based)

### False Positive Checklist

Before removing a "unused" dependency, verify it's not:

| Usage Pattern              | How to Check                                         |
| -------------------------- | ---------------------------------------------------- |
| Build tool / CLI           | Check `scripts` or `Makefile`                        |
| Plugin loaded by config    | Check config files (`.eslintrc`, `pytest.ini`, etc.) |
| Type-only dependency       | Check type annotation files                          |
| Conditional import         | Search for `try: import` or dynamic `__import__`     |
| Transitive peer dependency | Required by another package at runtime               |
| Test fixture               | Only used in test setup/teardown                     |
| Runtime plugin             | Loaded via entry points or plugin system             |

---

## Duplicate Functionality Detection

### Common Duplication Categories

| Category       | Duplicates Often Found                                   | Resolution                       |
| -------------- | -------------------------------------------------------- | -------------------------------- |
| HTTP clients   | requests, httpx, urllib3, aiohttp                        | Pick one (httpx if async needed) |
| JSON parsing   | json (stdlib), ujson, orjson, simplejson                 | stdlib unless perf-critical      |
| Date/time      | datetime (stdlib), arrow, pendulum, python-dateutil      | stdlib + dateutil for parsing    |
| Logging        | logging (stdlib), loguru, structlog                      | Pick one per project             |
| Config parsing | configparser, pydantic-settings, python-dotenv, dynaconf | Consolidate to one               |
| CLI frameworks | argparse, click, typer, fire                             | Pick one                         |
| Testing        | pytest, unittest, nose                                   | pytest (industry standard)       |
| Validation     | marshmallow, pydantic, cerberus, voluptuous              | Pick one                         |
| ORM            | SQLAlchemy, Django ORM, Peewee, Tortoise                 | Pick one per project             |

#### Node.js

| Category          | Duplicates Often Found             | Resolution                               |
| ----------------- | ---------------------------------- | ---------------------------------------- |
| HTTP clients      | axios, got, node-fetch, superagent | Pick one (fetch built-in Node 18+)       |
| Utility libraries | lodash, underscore, ramda          | Native JS methods where possible         |
| Date/time         | moment, dayjs, date-fns, luxon     | dayjs or date-fns (moment is deprecated) |
| Validation        | joi, yup, zod, ajv                 | Pick one per project                     |
| State management  | redux, mobx, zustand, jotai        | Pick one per project                     |

### Detection Approach

1. **Categorize each dependency** by primary function
2. **Flag categories with 2+ entries** as potential duplicates
3. **Verify actual overlap** — sometimes both are needed (e.g., one sync, one async)
4. **Recommend consolidation** — pick the one with better health metrics

---

## Heavy Transitive Tree Analysis

### Measuring Transitive Impact

For each direct dependency, count its transitive dependencies:

```text
# Python
uv pip install pipdeptree && uv run pipdeptree -p {package}

# Node.js
npm list {package} --all

# Rust
cargo tree -p {package}
```

### Red Flags

| Signal                 | Threshold                                  | Action                         |
| ---------------------- | ------------------------------------------ | ------------------------------ |
| Transitive count       | > 20 sub-dependencies                      | Investigate                    |
| Transitive count       | > 50 sub-dependencies                      | Strongly consider alternatives |
| Deep nesting           | > 5 levels deep                            | Fragile supply chain           |
| Unique transitive deps | Package pulls in deps used by nothing else | High marginal cost             |

### Heavy Package Analysis

Evaluate whether the transitive cost is justified:

```text
Justification Score = Feature Usage / Transitive Cost

Where:
  Feature Usage = (features used / features available)
  Transitive Cost = (unique transitive deps introduced)
```

Example:

```text
Package: pandas
  Features used: DataFrame.read_csv, DataFrame.to_json
  Features available: 500+ methods
  Transitive deps: numpy, python-dateutil, pytz, tzdata
  Unique transitive deps: 0 (all shared with other project deps)

  → Justified if DataFrame features are core to project
  → NOT justified if only parsing CSV (use stdlib csv instead)
```

### Common Heavy Packages

#### Python

| Package    | Typical Transitive Count | Lightweight Alternative         |
| ---------- | ------------------------ | ------------------------------- |
| pandas     | 4-5                      | polars (fewer deps), stdlib csv |
| boto3      | 3-4                      | None (required for AWS)         |
| django     | 3-4                      | flask, fastapi (lighter)        |
| tensorflow | 20+                      | pytorch, onnxruntime            |
| scipy      | 3-4                      | Specific algorithm packages     |

#### Node.js

| Package   | Typical Transitive Count | Lightweight Alternative                         |
| --------- | ------------------------ | ----------------------------------------------- |
| moment    | 0 (but 300KB)            | dayjs (2KB)                                     |
| lodash    | 0 (but 70KB)             | Native JS, lodash-es (tree-shake)               |
| express   | 30+                      | fastify, hono                                   |
| webpack   | 200+                     | esbuild, vite                                   |
| puppeteer | 50+ (+ Chromium binary)  | playwright (similar), cheerio (if no JS needed) |

---

## Size Analysis

### Measuring Package Size

| Metric                | Tool                               | Threshold                |
| --------------------- | ---------------------------------- | ------------------------ |
| Install size (disk)   | `du -sh node_modules/{pkg}`        | > 10MB is heavy          |
| Bundle size (browser) | bundlephobia.com, `npx bundlesize` | > 100KB gzipped is heavy |
| Download size         | Registry metadata                  | > 5MB is notable         |

### Size vs Usage Ratio

```text
Efficiency = Code Actually Used / Total Package Size

If efficiency < 10%:
  → Consider importing only needed submodules
  → Consider a lighter alternative
  → Consider copying the specific function needed (with attribution)
```

### Tree-Shaking Eligibility

| Condition                                    | Tree-Shakeable | Action                       |
| -------------------------------------------- | -------------- | ---------------------------- |
| ES modules (`import/export`)                 | Yes            | Use named imports            |
| CommonJS (`require/module.exports`)          | No             | Consider ESM alternative     |
| Side effects declared (`sideEffects: false`) | Yes            | Bundler can eliminate unused |
| Side effects present                         | Partially      | May include unused code      |

---

## Bloat Report Format

```text
### Bloat Analysis

#### Unused Dependencies
| Package | Declared In | Evidence | Recommendation |
|---------|------------|----------|----------------|
| {pkg} | {file} | No imports found in src/ | Remove |
| {pkg} | {file} | Only in unused test file | Remove or move to dev |

#### Duplicate Functionality
| Category | Packages | Recommendation |
|----------|----------|----------------|
| HTTP client | requests, httpx | Keep httpx, remove requests |
| Date parsing | arrow, python-dateutil | Keep dateutil, remove arrow |

#### Heavy Transitive Trees
| Package | Direct Use | Transitive Deps | Unique Deps | Justified |
|---------|-----------|-----------------|-------------|-----------|
| {pkg} | {what it's used for} | {count} | {count} | {Yes/No} |

#### Size Concerns
| Package | Install Size | Used Features | Recommendation |
|---------|-------------|--------------|----------------|
| {pkg} | {size} | {brief desc} | {Keep/Replace/Subset} |
```

---

## Removal Safety Checklist

Before removing a dependency flagged as bloat:

1. [ ] Verified no imports in source files (including dynamic imports)
2. [ ] Verified not used as CLI tool in scripts or CI
3. [ ] Verified not loaded as plugin via configuration
4. [ ] Verified not a peer dependency required by another package
5. [ ] Verified not used in test fixtures or setup
6. [ ] Run full test suite after removal
7. [ ] Check application startup after removal (runtime plugin loading)
