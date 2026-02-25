# Sizing Heuristics

Quick sizing patterns, complexity indicators, and reference class data for
rapid estimation.

---

## Quick Sizing Rules

### The "Lines of Integration" Heuristic

Count the number of external integration points:

| Integration Points | Typical Size |
|-------------------|-------------|
| 0 (pure logic) | S-M |
| 1 (one API, one DB) | M |
| 2-3 | M-L |
| 4+ | L-XL |

Each integration adds:
- Error handling
- Retry logic
- Configuration
- Testing with mocks

### The "Decision Count" Heuristic

Count the number of design decisions required:

| Decisions | Typical Size |
|-----------|-------------|
| 0 (follow existing pattern) | S |
| 1-2 (minor choices) | M |
| 3-5 (architectural choices) | L |
| 5+ (many unknowns) | XL |

### The "File Count" Heuristic

Count the number of files that need to change:

| Files | Typical Size |
|-------|-------------|
| 1-2 | S |
| 3-5 | M |
| 5-10 | L |
| 10+ | XL (or should be multiple tasks) |

---

## Reference Class Estimates

### Backend Tasks

| Task Type | Typical Size | Notes |
|-----------|-------------|-------|
| Add field to model | S (2h) | Schema + migration + API |
| New CRUD endpoint | M (8h) | Route + handler + validation + tests |
| New endpoint with logic | M-L (12h) | Above + business logic + edge cases |
| Authentication system | L (24h+) | Multiple endpoints, token management, security |
| File upload | M (8h) | Validation, storage, cleanup |
| Email/notification | M (8h) | Template, provider integration, queue |
| Search feature | L (20h) | Indexing, query parsing, ranking |
| Caching layer | M (8h) | Cache strategy, invalidation, testing |
| Rate limiting | M (6h) | Storage, middleware, headers |
| Webhook integration | M (8h) | Endpoint, verification, retry |

### Frontend Tasks

| Task Type | Typical Size | Notes |
|-----------|-------------|-------|
| Static page | S (2h) | Layout, styling |
| Form with validation | M (8h) | Fields, validation, submission, errors |
| Data table with sort/filter | M-L (12h) | Table, sorting, filtering, pagination |
| Modal/dialog | S (3h) | Component, open/close, content |
| Dashboard with charts | L (16h) | Data fetching, chart components, layout |
| Responsive redesign | L (20h) | Breakpoints, layout changes, testing |

### Infrastructure Tasks

| Task Type | Typical Size | Notes |
|-----------|-------------|-------|
| CI pipeline setup | M (8h) | Build, test, deploy stages |
| Docker containerization | M (8h) | Dockerfile, compose, testing |
| Database migration (schema only) | S (2h) | ALTER statements |
| Database migration (with data) | M-L (12h) | Data transformation, validation |
| Monitoring/alerting setup | M (8h) | Metrics, dashboards, alert rules |
| Secret management | M (8h) | Vault/KMS integration, rotation |

---

## Effort Multipliers

Apply these to the base estimate:

| Factor | Multiplier | When |
|--------|-----------|------|
| First time with technology | 2.0x | Never used this library/framework |
| Second time | 1.3x | Used once before |
| Third+ time | 1.0x | Familiar pattern |
| Security-sensitive | 1.5x | Auth, crypto, PII handling |
| Cross-team coordination | 1.3x | Need input/approval from another team |
| Legacy codebase | 1.3-2.0x | Poor documentation, no tests |
| High test coverage requirement | 1.3x | 90%+ coverage target |
| Accessibility requirements | 1.2x | WCAG compliance |

---

## "Should I Estimate or Spike?"

| Condition | Action |
|-----------|--------|
| Less than 2 unknowns, familiar stack | Estimate directly |
| 2-3 unknowns, partial familiarity | Estimate with wide range (3x spread) |
| 4+ unknowns, new technology | Spike first (1-2 days), then estimate |
| "I have no idea" | Definitely spike first |

A spike is a timeboxed investigation to reduce uncertainty. The output is information
(and a narrower estimate), not code.
