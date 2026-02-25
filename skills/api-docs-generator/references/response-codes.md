# Response Codes

Standard HTTP response codes for REST API documentation with descriptions and
usage guidelines.

---

## Success Codes (2xx)

| Code | Name | When to Use | Response Body |
|------|------|-------------|---------------|
| 200 | OK | Successful GET, PUT, PATCH | Resource or result |
| 201 | Created | Successful POST that created a resource | Created resource |
| 202 | Accepted | Async operation accepted, not yet complete | Status/tracking info |
| 204 | No Content | Successful DELETE, or action with no response | None |

### Documentation Pattern

```python
# 200: Standard response
responses={200: {"description": "Returns the requested resource"}}

# 201: Created
responses={201: {"description": "Resource created successfully", "model": Resource}}

# 204: No content
responses={204: {"description": "Resource deleted successfully"}}
```

---

## Client Error Codes (4xx)

| Code | Name | When to Use | Documentation Notes |
|------|------|-------------|---------------------|
| 400 | Bad Request | Malformed request body or query | Describe what makes a request invalid |
| 401 | Unauthorized | Missing or invalid authentication | Document auth requirements |
| 403 | Forbidden | Authenticated but insufficient permissions | Document required roles/permissions |
| 404 | Not Found | Resource does not exist | Document which identifier was not found |
| 405 | Method Not Allowed | HTTP method not supported for this endpoint | Usually auto-documented |
| 409 | Conflict | Action conflicts with current state | Document what state causes conflict |
| 410 | Gone | Resource was deleted and will not return | Distinguish from 404 |
| 422 | Unprocessable Entity | Validation error (FastAPI default) | FastAPI auto-documents this |
| 429 | Too Many Requests | Rate limit exceeded | Document rate limit policy |

### Common Error Response Schema

```python
class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Human-readable error message")
    code: str = Field(..., description="Machine-readable error code")

# Usage in endpoint
responses={
    400: {
        "description": "Invalid request parameters",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {
                    "detail": "Start date must be before end date",
                    "code": "INVALID_DATE_RANGE",
                }
            }
        },
    },
}
```

---

## Server Error Codes (5xx)

| Code | Name | When to Document | Notes |
|------|------|-----------------|-------|
| 500 | Internal Server Error | Generally NOT documented | Users can't act on it |
| 502 | Bad Gateway | If behind proxy/gateway | Document retry strategy |
| 503 | Service Unavailable | During maintenance | Document expected availability |
| 504 | Gateway Timeout | Long-running operations | Document timeout limits |

**General rule:** Don't document 500 errors — they indicate a bug, not an expected
condition. Document 502/503/504 only if users need to handle them.

---

## REST Method → Expected Codes

| Method | Success | Common Errors |
|--------|---------|---------------|
| GET (single) | 200 | 401, 403, 404 |
| GET (list) | 200 | 401, 403, 422 (bad filter params) |
| POST (create) | 201 | 400, 401, 403, 409, 422 |
| PUT (replace) | 200 | 400, 401, 403, 404, 422 |
| PATCH (update) | 200 | 400, 401, 403, 404, 422 |
| DELETE | 204 | 401, 403, 404 |

---

## Pagination Response Pattern

```python
class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int = Field(..., description="Total items matching query", example=150)
    page: int = Field(..., description="Current page number", example=1)
    per_page: int = Field(..., description="Items per page", example=20)
    pages: int = Field(..., description="Total pages", example=8)

# Document link headers if using them
responses={
    200: {
        "description": "Paginated list of users",
        "headers": {
            "Link": {
                "description": "Pagination links (next, prev, first, last)",
                "schema": {"type": "string"},
            },
            "X-Total-Count": {
                "description": "Total number of items",
                "schema": {"type": "integer"},
            },
        },
    },
}
```

---

## Error Code Naming Conventions

Use consistent, machine-readable error codes:

| Pattern | Examples |
|---------|---------|
| `{RESOURCE}_NOT_FOUND` | `USER_NOT_FOUND`, `ORDER_NOT_FOUND` |
| `{RESOURCE}_{CONFLICT}` | `EMAIL_EXISTS`, `USERNAME_TAKEN` |
| `INVALID_{FIELD}` | `INVALID_EMAIL`, `INVALID_DATE_RANGE` |
| `MISSING_{FIELD}` | `MISSING_AUTHORIZATION`, `MISSING_BODY` |
| `{ACTION}_FAILED` | `PAYMENT_FAILED`, `UPLOAD_FAILED` |
| `RATE_LIMIT_EXCEEDED` | Self-explanatory |
| `INSUFFICIENT_PERMISSIONS` | Self-explanatory |
