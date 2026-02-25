# Sizing Guide

Effort estimation heuristics for task sizing during decomposition.

---

## T-Shirt Sizes

| Size | Duration | Lines of Code | Complexity |
|------|----------|---------------|------------|
| S (Small) | < 4 hours | < 100 | Single function, clear requirements |
| M (Medium) | 4-16 hours | 100-500 | Multiple functions, some decisions |
| L (Large) | 16-40 hours | 500-2000 | Multiple files, design decisions |
| XL (Extra Large) | > 40 hours | > 2000 | MUST decompose further |

---

## Complexity Indicators

### Factors That Increase Size

| Factor | Impact | Example |
|--------|--------|---------|
| New technology | +1 size | First time using WebSockets |
| External API integration | +1 size | Third-party payment API |
| Data migration | +1 size | Transforming existing data |
| Security requirements | +1 size | Auth, encryption, audit logging |
| Backward compatibility | +1 size | Must support old and new format |
| Multiple edge cases | +1 size | Complex validation rules |
| Concurrency | +1-2 sizes | Race conditions, locks |

### Factors That Decrease Size

| Factor | Impact | Example |
|--------|--------|---------|
| Existing pattern | -1 size | CRUD endpoint matching existing ones |
| Library handles complexity | -1 size | Using ORM instead of raw SQL |
| Clear specification | -1 size | Detailed requirements with examples |
| Team familiarity | -1 size | Done something similar recently |

---

## Reference Tasks

Use known-complexity tasks as anchors:

| Reference Task | Typical Size |
|---------------|-------------|
| Add a new field to an existing model | S |
| New CRUD endpoint (standard pattern) | M |
| New API endpoint with business logic | M-L |
| Database migration with data backfill | M-L |
| Third-party API integration | L |
| Authentication system | L-XL |
| Search functionality | L |
| File upload with validation | M |
| Email notification system | M-L |
| Caching layer | M |
| Rate limiting | M |
| Pagination | S-M |

---

## Estimation Biases

### Planning Fallacy

People consistently underestimate by 25-50%. Counteract by:
- Comparing to similar past tasks (reference class forecasting)
- Using three-point estimation (best/likely/worst)
- Adding buffer for unknowns (20% minimum)

### Anchoring

First estimate heard becomes the anchor. Counteract by:
- Estimate independently before discussing
- Use bottom-up (task-level) estimation, not top-down

### Optimism Bias

"It'll be straightforward" → it rarely is. Counteract by:
- List specific unknowns for each task
- Ask: "What could go wrong?"
- Check: "What took longer than expected last time?"

---

## From Size to Duration

### Solo Developer

| Size | Calendar Days | Working Hours |
|------|--------------|---------------|
| S | 0.5-1 | 2-4 |
| M | 1-2 | 4-16 |
| L | 2-5 | 16-40 |

### Team (with review/communication overhead)

| Size | Calendar Days | Notes |
|------|--------------|-------|
| S | 1 | Including code review |
| M | 2-3 | Including review and revision |
| L | 3-5 | Including design discussion |

Add 20% for context switching if working on multiple tasks.
