# Example Generation

Creating realistic, representative examples for API documentation using Pydantic
models and OpenAPI schema extras.

---

## Principles

1. **Realistic over generic.** `"alice@example.com"` not `"string"`. `42` not `0`.
2. **Consistent within a model.** If the user is "Alice Smith", their email is
   `alice.smith@example.com`, not `user@test.com`.
3. **Varied across models.** Different endpoints should show different example data
   to demonstrate the range of valid values.
4. **Valid against constraints.** Examples must pass the model's own validation rules.
5. **Safe for documentation.** No real email addresses, phone numbers, or PII.

---

## Pydantic Model Examples

### Field-Level Examples

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(..., description="Unique user identifier", example=42)
    name: str = Field(..., description="Full name", example="Alice Smith")
    email: str = Field(..., description="Email address", example="alice@example.com")
    role: str = Field("member", description="User role", example="admin")
    active: bool = Field(True, description="Account active status", example=True)
```

### Model-Level Examples (json_schema_extra)

```python
from pydantic import BaseModel, ConfigDict

class Order(BaseModel):
    id: int
    user_id: int
    total: float
    status: str
    items: list[OrderItem]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1001,
                "user_id": 42,
                "total": 99.99,
                "status": "completed",
                "items": [
                    {"product_id": 5, "quantity": 2, "price": 29.99},
                    {"product_id": 12, "quantity": 1, "price": 40.01},
                ],
            }
        }
    )
```

### Multiple Examples

```python
class UserCreate(BaseModel):
    name: str
    email: str
    role: str = "member"

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Alice Smith",
                    "email": "alice@example.com",
                    "role": "member",
                },
                {
                    "name": "Bob Admin",
                    "email": "bob@example.com",
                    "role": "admin",
                },
            ]
        }
    )
```

---

## Example Values by Type

### Strings

| Field Purpose | Example Value |
|--------------|---------------|
| Name (person) | `"Alice Smith"`, `"Bob Johnson"` |
| Email | `"alice@example.com"`, `"bob.johnson@company.org"` |
| Username | `"alice_smith"`, `"bjohnson"` |
| URL | `"https://example.com/resource"` |
| Description | `"A detailed description of the item"` |
| UUID | `"550e8400-e29b-41d4-a716-446655440000"` |
| Date (ISO) | `"2026-02-25"` |
| Datetime (ISO) | `"2026-02-25T14:30:00Z"` |
| Phone | `"+1-555-123-4567"` |
| Address | `"123 Main St, Springfield, IL 62701"` |
| Color (hex) | `"#FF5733"` |
| File path | `"/documents/report.pdf"` |
| API key | `"sk_live_abc123..."` (truncated) |

### Numbers

| Field Purpose | Example Value |
|--------------|---------------|
| ID | `42`, `1001` (avoid `0` and `1`) |
| Count | `15`, `100` |
| Price | `29.99`, `99.95` |
| Percentage | `75.5`, `42.0` |
| Age | `28`, `35` |
| Latitude | `37.7749` |
| Longitude | `-122.4194` |
| Port | `8080`, `5432` |

### Collections

| Field Purpose | Example Value |
|--------------|---------------|
| Tags | `["python", "api", "rest"]` |
| Roles | `["admin", "editor"]` |
| IDs | `[1, 2, 3]` |
| Empty allowed | `[]` (show both empty and populated examples) |

---

## Request/Response Example Pairs

Document matching request and response examples:

```python
# Request example
{
    "name": "Alice Smith",
    "email": "alice@example.com",
    "role": "member"
}

# Response example (includes generated fields)
{
    "id": 42,
    "name": "Alice Smith",
    "email": "alice@example.com",
    "role": "member",
    "created_at": "2026-02-25T14:30:00Z",
    "active": True
}
```

The response example should include all fields the request example has, plus
server-generated fields (id, timestamps, computed fields).

---

## Error Response Examples

```python
# 400 Bad Request
{
    "detail": "Invalid email format",
    "code": "INVALID_EMAIL"
}

# 404 Not Found
{
    "detail": "User with id 999 not found",
    "code": "USER_NOT_FOUND"
}

# 409 Conflict
{
    "detail": "Email alice@example.com is already registered",
    "code": "EMAIL_EXISTS"
}

# 422 Validation Error (FastAPI default)
{
    "detail": [
        {
            "loc": ["body", "email"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```
