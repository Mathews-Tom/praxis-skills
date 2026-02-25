# SQL Anti-Patterns

Common SQL performance anti-patterns with detection rules, impact analysis, and fixes.

---

## Query-Level Anti-Patterns

### 1. SELECT *

```sql
-- BAD
SELECT * FROM users WHERE id = 42;

-- GOOD
SELECT id, name, email FROM users WHERE id = 42;
```

**Impact:** Fetches all columns including large TEXT/BLOB fields. Prevents covering
index optimization. Increases network transfer and memory usage.

**Detection:** Star (`*`) in SELECT clause.

**Fix:** List only the columns needed by the application.

### 2. Function on Indexed Column

```sql
-- BAD: Index on email is bypassed
SELECT * FROM users WHERE UPPER(email) = 'ALICE@EXAMPLE.COM';

-- GOOD: Index on email is used
SELECT * FROM users WHERE email = 'alice@example.com';

-- If case-insensitive needed (PostgreSQL):
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';
```

**Impact:** Applying a function to an indexed column prevents index usage. The database
must scan every row and apply the function.

**Detection:** Function call wrapping a WHERE column (`UPPER()`, `LOWER()`, `DATE()`,
`CAST()`, `COALESCE()`).

### 3. Implicit Type Cast

```sql
-- BAD: phone is VARCHAR, comparing to integer
SELECT * FROM users WHERE phone = 5551234567;

-- GOOD: Compare with matching types
SELECT * FROM users WHERE phone = '5551234567';
```

**Impact:** Type mismatch forces implicit casting, which may bypass the index.

**Detection:** Column type doesn't match the literal or parameter type.

### 4. Leading Wildcard LIKE

```sql
-- BAD: Leading wildcard, full scan
SELECT * FROM products WHERE name LIKE '%widget%';

-- GOOD: Trailing wildcard only, index usable
SELECT * FROM products WHERE name LIKE 'widget%';

-- For full-text search, use dedicated feature
SELECT * FROM products WHERE to_tsvector('english', name) @@ to_tsquery('widget');
```

**Impact:** `LIKE '%text'` or `LIKE '%text%'` cannot use B-tree indexes. Full table scan.

### 5. OR Across Different Columns

```sql
-- BAD: OR prevents single index use
SELECT * FROM orders WHERE user_id = 42 OR status = 'pending';

-- GOOD: UNION uses separate indexes
SELECT * FROM orders WHERE user_id = 42
UNION
SELECT * FROM orders WHERE status = 'pending';
```

**Impact:** OR conditions on different columns prevent the optimizer from using a single
index efficiently. May result in full table scan.

### 6. N+1 Queries (Correlated Subquery)

```sql
-- BAD: N+1 — subquery runs once per order row
SELECT o.id,
       (SELECT u.name FROM users u WHERE u.id = o.user_id) AS user_name
FROM orders o;

-- GOOD: Single JOIN
SELECT o.id, u.name AS user_name
FROM orders o
JOIN users u ON u.id = o.user_id;
```

**Impact:** Correlated subquery executes once per row in the outer query. For 10K orders,
this runs 10K separate user lookups.

### 7. SELECT DISTINCT as a Band-Aid

```sql
-- BAD: DISTINCT hides a duplicate-producing join
SELECT DISTINCT u.name, u.email
FROM users u
JOIN orders o ON o.user_id = u.id;

-- GOOD: EXISTS avoids duplicates at the source
SELECT u.name, u.email
FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);
```

**Impact:** DISTINCT sorts and deduplicates the entire result set. Often indicates
the JOIN produces unintended duplicates — fix the query, not the symptom.

### 8. Missing WHERE on JOIN

```sql
-- BAD: Cartesian product
SELECT * FROM users, orders;

-- GOOD: Explicit join condition
SELECT * FROM users JOIN orders ON orders.user_id = users.id;
```

**Impact:** Without a join condition, the result is the cross product of both tables.
1K users × 10K orders = 10M rows.

### 9. COUNT(*) for Existence Check

```sql
-- BAD: Counts all matching rows
IF (SELECT COUNT(*) FROM orders WHERE user_id = 42) > 0

-- GOOD: Stops at first match
IF EXISTS (SELECT 1 FROM orders WHERE user_id = 42)
```

**Impact:** COUNT(*) scans all matching rows. EXISTS stops at the first match.

### 10. Unnecessary Sorting

```sql
-- BAD: ORDER BY on unindexed column for large result
SELECT * FROM logs ORDER BY created_at DESC LIMIT 100;

-- GOOD: Index supports the sort
CREATE INDEX idx_logs_created ON logs(created_at DESC);
SELECT * FROM logs ORDER BY created_at DESC LIMIT 100;
```

**Impact:** Without an index matching ORDER BY, the database must sort the entire
result set in memory (or disk for large results) before returning LIMIT rows.
