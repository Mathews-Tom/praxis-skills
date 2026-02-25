# Edge Case Checklist

Common edge cases organized by domain. Use as a prompt when identifying edge cases
during task decomposition.

---

## Input Edge Cases

### Strings

| Edge Case | Test |
|-----------|------|
| Empty string | `""` |
| Whitespace only | `"   "`, `"\t\n"` |
| Very long string | 10K+ characters |
| Unicode | Emoji, CJK, RTL, combining characters |
| Special characters | `<script>`, `'; DROP TABLE`, `../` |
| Null/None | `None`, `null` |
| HTML entities | `&amp;`, `&lt;` |
| Control characters | `\0`, `\x00` |

### Numbers

| Edge Case | Test |
|-----------|------|
| Zero | `0`, `0.0` |
| Negative | `-1`, `-0.0` |
| Maximum | `sys.maxsize`, `Number.MAX_SAFE_INTEGER` |
| Float precision | `0.1 + 0.2` |
| NaN / Infinity | `float('nan')`, `float('inf')` |
| Very small | `0.000001` |
| Boundary ±1 | Off-by-one at every boundary |

### Collections

| Edge Case | Test |
|-----------|------|
| Empty | `[]`, `{}` |
| Single element | `[1]`, `{"a": 1}` |
| Duplicate elements | `[1, 1, 1]` |
| Very large | 100K+ elements |
| Nested | Deeply nested structures |
| Mixed types | `[1, "two", None, 3.0]` |

### Dates and Times

| Edge Case | Test |
|-----------|------|
| Midnight | `00:00:00` |
| End of day | `23:59:59` |
| Leap year | Feb 29 |
| Timezone changes | DST transitions |
| Epoch | `1970-01-01` |
| Far future | Year 2038, year 9999 |
| Invalid dates | Feb 30, month 13 |

---

## State Edge Cases

### Concurrency

| Edge Case | Scenario |
|-----------|----------|
| Simultaneous writes | Two users edit the same record |
| Read during write | Query returns partial update |
| Double submit | Form submitted twice quickly |
| Stale data | Data changed between read and write |
| Lost update | Last write wins, first write lost |

### Lifecycle

| Edge Case | Scenario |
|-----------|----------|
| First use | No data exists yet (empty state) |
| Re-initialization | System restarted mid-operation |
| Migration | Old data format meets new code |
| Rollback | Feature disabled after some users used it |
| Partial completion | Operation interrupted midway |

---

## Web/API Edge Cases

### HTTP

| Edge Case | Scenario |
|-----------|----------|
| Timeout | Request takes > configured timeout |
| 4xx response | Client error from downstream service |
| 5xx response | Server error from downstream service |
| Empty response body | 200 OK but no content |
| Large payload | Request/response exceeds size limits |
| Slow response | Connection established but data trickles |
| DNS failure | Cannot resolve hostname |
| Certificate error | Expired/invalid TLS cert |

### Authentication

| Edge Case | Scenario |
|-----------|----------|
| Expired token | Valid but expired |
| Revoked token | Was valid, now revoked |
| No token | Request without auth header |
| Malformed token | Random string, wrong format |
| Different user | Token for user A used to access user B's data |

### Pagination

| Edge Case | Scenario |
|-----------|----------|
| Page 0 | Some APIs are 0-indexed, some 1-indexed |
| Last page | Partial page, fewer items than per_page |
| Beyond last page | Page number exceeds total pages |
| Data changes between pages | New items added/removed during pagination |
| Very large per_page | Per_page=1000000 |

---

## Database Edge Cases

| Edge Case | Scenario |
|-----------|----------|
| NULL values | Column allows NULL, code doesn't handle it |
| Foreign key violation | Referenced row doesn't exist |
| Unique constraint | Duplicate insert |
| Deadlock | Two transactions lock each other |
| Connection pool exhaustion | All connections in use |
| Long-running query | Query blocks other operations |

---

## File System Edge Cases

| Edge Case | Scenario |
|-----------|----------|
| File not found | Expected file doesn't exist |
| Permission denied | File exists but not readable |
| Empty file | File exists but has zero bytes |
| Very large file | Exceeds available memory |
| Symbolic link | File is a symlink (follow or not?) |
| Concurrent access | Another process modifying the file |
| Disk full | Write fails mid-operation |
| Path traversal | `../../etc/passwd` in filename |
