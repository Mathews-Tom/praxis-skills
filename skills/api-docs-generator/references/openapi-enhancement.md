# OpenAPI Enhancement

Techniques for enriching OpenAPI specifications beyond what frameworks auto-generate:
tags, schema documentation, security schemes, and external docs.

---

## Tag Organization

### Defining Tags

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Users",
            "description": "User account management — create, read, update, delete",
        },
        {
            "name": "Orders",
            "description": "Order processing and history",
        },
        {
            "name": "Auth",
            "description": "Authentication and token management",
        },
        {
            "name": "Admin",
            "description": "Administrative operations. Requires admin role.",
        },
    ],
)
```

### Tag Assignment Rules

| Rule | Example |
|------|---------|
| One primary tag per endpoint | `tags=["Users"]` not `tags=["Users", "Admin"]` |
| Tag names are nouns | "Users" not "Get Users" |
| Order tags by importance | Most-used tags first |
| Group CRUD by resource | All `/users/*` endpoints share the "Users" tag |

---

## Schema Documentation

### Enum Documentation

```python
from enum import Enum

class OrderStatus(str, Enum):
    """Order processing status."""
    pending = "pending"      # Order created, awaiting payment
    paid = "paid"            # Payment received, awaiting fulfillment
    shipped = "shipped"      # Order shipped, tracking available
    delivered = "delivered"  # Order delivered
    cancelled = "cancelled"  # Order cancelled by user or system
```

### Discriminated Unions

```python
from pydantic import BaseModel, Field
from typing import Literal

class CreditCardPayment(BaseModel):
    type: Literal["credit_card"] = "credit_card"
    card_last4: str = Field(..., description="Last 4 digits", example="4242")
    exp_month: int = Field(..., description="Expiration month", example=12)
    exp_year: int = Field(..., description="Expiration year", example=2027)

class BankTransferPayment(BaseModel):
    type: Literal["bank_transfer"] = "bank_transfer"
    account_last4: str = Field(..., description="Last 4 digits", example="6789")
    routing: str = Field(..., description="Routing number", example="021000021")

Payment = CreditCardPayment | BankTransferPayment
```

---

## Security Scheme Documentation

### Bearer Token

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(
    scheme_name="BearerAuth",
    description="JWT Bearer token. Obtain via POST /auth/login.",
)
```

### API Key

```python
from fastapi.security import APIKeyHeader

api_key = APIKeyHeader(
    name="X-API-Key",
    description="API key for service-to-service authentication. "
    "Request keys via the developer portal.",
)
```

### OAuth2

```python
from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={
        "read:users": "Read user information",
        "write:users": "Create and modify users",
        "admin": "Full administrative access",
    },
)
```

---

## API Metadata

```python
app = FastAPI(
    title="Order Management API",
    description="""
    ## Overview

    The Order Management API provides endpoints for managing customer orders,
    processing payments, and tracking delivery.

    ## Authentication

    All endpoints require a Bearer token obtained via `POST /auth/login`.
    Include the token in the `Authorization` header:

    ```
    Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
    ```

    ## Rate Limiting

    - Standard tier: 100 requests/minute
    - Premium tier: 1000 requests/minute

    Rate limit headers are included in all responses:
    - `X-RateLimit-Limit`: Maximum requests per window
    - `X-RateLimit-Remaining`: Remaining requests
    - `X-RateLimit-Reset`: Window reset time (Unix timestamp)
    """,
    version="2.1.0",
    terms_of_service="https://example.com/terms",
    contact={
        "name": "API Support",
        "url": "https://example.com/support",
        "email": "api-support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)
```

---

## External Documentation Links

```python
@router.get(
    "/reports",
    external_docs={
        "description": "Report format specification",
        "url": "https://docs.example.com/reports",
    },
)
```

---

## Custom OpenAPI Schema Modifications

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add custom server URLs
    openapi_schema["servers"] = [
        {"url": "https://api.example.com", "description": "Production"},
        {"url": "https://staging-api.example.com", "description": "Staging"},
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

---

## Documentation Completeness Checklist

For each endpoint:
- [ ] Has summary (short) and description (detailed)
- [ ] All path parameters have descriptions and examples
- [ ] All query parameters have descriptions, examples, and defaults
- [ ] Request body has model with field descriptions and examples
- [ ] All possible response codes documented
- [ ] Error responses have model and example
- [ ] Assigned to appropriate tag
- [ ] Authentication requirements documented
- [ ] Deprecation noted if applicable
