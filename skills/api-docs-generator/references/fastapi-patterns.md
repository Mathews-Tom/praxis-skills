# FastAPI Documentation Patterns

FastAPI-specific patterns for endpoint documentation, parameter metadata, and
OpenAPI spec enhancement.

---

## Endpoint Documentation

### Docstring → OpenAPI Description

FastAPI uses the handler's docstring as the endpoint description in OpenAPI:

```python
@router.get("/users/{user_id}")
async def get_user(user_id: int) -> User:
    """
    Retrieve a user by their unique identifier.

    Returns the user's profile information including name, email,
    and account status. Requires authentication.
    """
```

### Summary vs Description

```python
@router.get(
    "/users/{user_id}",
    summary="Get user by ID",           # Short, appears in endpoint list
    description="Detailed description",  # Long, appears in expanded view
)
```

If both `summary` and docstring exist, `summary` takes precedence for the short
label. The docstring becomes the description.

---

## Parameter Documentation

### Path Parameters

```python
from fastapi import Path

@router.get("/users/{user_id}")
async def get_user(
    user_id: int = Path(
        ...,
        description="Unique user identifier",
        example=42,
        ge=1,
    ),
) -> User:
    ...
```

### Query Parameters

```python
from fastapi import Query

@router.get("/users")
async def list_users(
    page: int = Query(1, description="Page number", ge=1, example=1),
    per_page: int = Query(20, description="Items per page", ge=1, le=100, example=20),
    status: str | None = Query(None, description="Filter by status", example="active"),
    sort_by: str = Query("created_at", description="Sort field", example="name"),
) -> list[User]:
    ...
```

### Header Parameters

```python
from fastapi import Header

@router.get("/users/me")
async def get_current_user(
    authorization: str = Header(..., description="Bearer token", example="Bearer eyJ..."),
    x_request_id: str | None = Header(None, description="Request trace ID"),
) -> User:
    ...
```

### Request Body

```python
from fastapi import Body

@router.post("/users")
async def create_user(
    user: UserCreate = Body(
        ...,
        examples=[
            {
                "summary": "Standard user",
                "value": {
                    "name": "Alice Smith",
                    "email": "alice@example.com",
                    "role": "member",
                },
            },
            {
                "summary": "Admin user",
                "value": {
                    "name": "Bob Admin",
                    "email": "bob@example.com",
                    "role": "admin",
                },
            },
        ],
    ),
) -> User:
    ...
```

---

## Response Documentation

### Status Codes

```python
@router.post(
    "/users",
    status_code=201,
    response_model=User,
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid input data"},
        409: {"description": "Email already registered"},
        422: {"description": "Validation error"},
    },
)
```

### Response Models for Error Codes

```python
class ErrorResponse(BaseModel):
    detail: str = Field(..., example="User not found")
    code: str = Field(..., example="USER_NOT_FOUND")

@router.get(
    "/users/{user_id}",
    responses={
        404: {
            "description": "User not found",
            "model": ErrorResponse,
        },
    },
)
```

### Multiple Response Models

```python
@router.get(
    "/users/{user_id}",
    response_model=User,
    responses={
        200: {
            "description": "User found",
            "content": {
                "application/json": {
                    "example": {
                        "id": 42,
                        "name": "Alice Smith",
                        "email": "alice@example.com",
                    }
                }
            },
        },
    },
)
```

---

## Tags and Grouping

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={401: {"description": "Not authenticated"}},
)
```

### Tag Metadata (in main app)

```python
app = FastAPI(
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operations with user accounts",
        },
        {
            "name": "Orders",
            "description": "Order management operations",
        },
    ],
)
```

---

## Deprecation

```python
@router.get(
    "/users/{user_id}/profile",
    deprecated=True,
    summary="Get user profile (deprecated)",
    description="Use GET /users/{user_id} instead. Will be removed in v3.0.",
)
```

---

## Authentication Documentation

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@router.get("/users/me")
async def get_me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """
    Get the currently authenticated user.

    Requires a valid Bearer token in the Authorization header.
    """
```
