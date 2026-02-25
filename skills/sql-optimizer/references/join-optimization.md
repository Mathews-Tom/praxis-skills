# Join Optimization

Join type selection, join order optimization, and subquery-to-join conversion patterns.

---

## Join Types

### INNER JOIN vs LEFT JOIN

```sql
-- INNER JOIN: Only matching rows from both tables
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON o.user_id = u.id;
-- Users with no orders are excluded

-- LEFT JOIN: All rows from left table, NULLs for non-matches
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON o.user_id = u.id;
-- Users with no orders appear with NULL total
```

**Performance rule:** INNER JOIN is generally faster because the optimizer has more
freedom to reorder tables. Use LEFT JOIN only when you need unmatched rows.

### Self-Join

```sql
-- Find employees and their managers
SELECT e.name AS employee, m.name AS manager
FROM employees e
JOIN employees m ON m.id = e.manager_id;
```

Ensure the join column (manager_id) is indexed.

### Cross Join (Cartesian Product)

```sql
-- Intentional: Generate all combinations
SELECT s.size, c.color
FROM sizes s
CROSS JOIN colors c;
```

Cross joins are almost never intentional in analytical queries. If you see one,
check for a missing join condition.

---

## Join Order

### How Optimizers Choose Order

The query optimizer evaluates different join orders and picks the cheapest. You can
influence this with:

1. **Statistics accuracy** — Run `ANALYZE` so the optimizer has correct row counts
2. **Index availability** — Indexes on join columns enable efficient lookups
3. **Filter placement** — Filter early to reduce intermediate result sizes

### Manual Join Order Hints

```sql
-- PostgreSQL: Disable join reordering for debugging
SET join_collapse_limit = 1;

-- MySQL: STRAIGHT_JOIN forces left-to-right order
SELECT STRAIGHT_JOIN ...
FROM small_table s
JOIN large_table l ON l.id = s.large_id;
```

Use hints only for debugging. Let the optimizer choose in production.

---

## Subquery-to-JOIN Conversion

### Correlated Subquery → JOIN

```sql
-- BAD: Correlated subquery (N+1)
SELECT o.id, o.total,
       (SELECT u.name FROM users u WHERE u.id = o.user_id)
FROM orders o;

-- GOOD: JOIN
SELECT o.id, o.total, u.name
FROM orders o
JOIN users u ON u.id = o.user_id;
```

### IN (SELECT ...) → EXISTS or JOIN

```sql
-- Subquery
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 100);

-- EXISTS (often faster, stops at first match)
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.user_id = u.id AND o.total > 100
);

-- JOIN (use when you need columns from both tables)
SELECT DISTINCT u.*
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.total > 100;
```

### NOT IN → NOT EXISTS

```sql
-- BAD: NOT IN has NULL trap — if subquery returns any NULL, result is empty
SELECT * FROM users
WHERE id NOT IN (SELECT user_id FROM deleted_users);

-- GOOD: NOT EXISTS handles NULLs correctly
SELECT * FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM deleted_users d WHERE d.user_id = u.id
);

-- GOOD: LEFT JOIN with NULL check
SELECT u.*
FROM users u
LEFT JOIN deleted_users d ON d.user_id = u.id
WHERE d.user_id IS NULL;
```

---

## CTE (Common Table Expression) Performance

### PostgreSQL CTE Behavior

| PostgreSQL Version | CTE Behavior |
|-------------------|-------------|
| < 12 | Always materialized (optimization fence) |
| >= 12 | Inlined by default if referenced once |

```sql
-- Force materialization (PostgreSQL 12+)
WITH cte AS MATERIALIZED (
    SELECT * FROM large_table WHERE condition
)
SELECT * FROM cte;

-- Force inlining (PostgreSQL 12+)
WITH cte AS NOT MATERIALIZED (
    SELECT * FROM large_table WHERE condition
)
SELECT * FROM cte;
```

### MySQL CTE Behavior

MySQL 8.0+ supports CTEs. They are generally materialized as temporary tables.
For performance-critical queries, consider replacing CTEs with subqueries or
temporary tables.

---

## Join Optimization Checklist

1. **Index join columns** — Both sides of the join condition should have indexes
2. **Filter before joining** — Move WHERE conditions as close to the source table as possible
3. **Use INNER JOIN when possible** — More optimization freedom than LEFT JOIN
4. **Avoid implicit joins** — Use explicit JOIN syntax for clarity
5. **Watch for cartesian products** — Every JOIN should have an ON condition
6. **Convert N+1 subqueries to JOINs** — Single query instead of N queries
7. **Prefer EXISTS over IN for existence checks** — Stops at first match
8. **Use NOT EXISTS instead of NOT IN** — Correct NULL handling
