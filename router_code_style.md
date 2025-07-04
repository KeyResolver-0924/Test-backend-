# FastAPI Router Code Style Guide

This guide outlines the standard structure and patterns for FastAPI routers in our codebase.

## File Structure

```python
# 1. Imports (grouped logically)
from fastapi import ...
from typing import ...
import logging
# Local imports last
from ..schemas import ...
from ..config import ...
from ..dependencies import ...
from ..utils import ...

# 2. Router Configuration
router = APIRouter(
    prefix="",
    tags=["resource-name"],
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "Resource not found"},
        409: {"description": "Conflict with existing resource"},
        500: {"description": "Internal server error"}
    }
)

# 3. Helper Functions
async def get_resource_by_id(...):
    """Helper functions for common operations"""
    pass

# 4. CRUD Endpoints (in standard order)
# Create, Read, Update, Delete
```

## Code Organization

1. **Directory Structure**:
   ```
   src/api/
   ├── dependencies/     # FastAPI dependency injections
   ├── utils/           # General purpose utilities
   └── routers/         # API routes
   ```

2. **Endpoint Order**:
   - Create (POST)
   - Read (GET list + GET detail)
   - Update (PUT/PATCH)
   - Delete (DELETE)

## Documentation Standards

### Endpoint Documentation
```python
@router.method(
    path="/{param}",
    response_model=ResponseModel,
    summary="Concise action description",
    description="""
    Detailed description of the endpoint.
    
    Returns:
    - 200: Success case
    - 404: Not found case
    - etc.
    """
)
```

### Function Documentation
```python
async def function_name(param: type) -> return_type:
    """
    Concise description.
    
    Args:
        param: description
        
    Returns:
        description
        
    Raises:
        HTTPException: conditions
    """
```

## Error Handling

1. **Use Supabase Handler (available in utils/supabase.py**:
```python
result = await handle_supabase_operation(
    operation_name="descriptive operation name",
    operation=supabase.from_("table").select("*"),
    error_msg="User-friendly error message"
)
```

2. **HTTP Exceptions**:
   - Use appropriate status codes
   - Provide clear error messages
   - Include context when needed

## Logging

1. **Success Logging**:
```python
logger.info(f"Successfully completed {operation}")
```

2. **Warning for Business Rules**:
```python
logger.warning(
    f"Business rule violation",
    extra={"context": "details"}
)
```

3. **Error Logging**:
```python
logger.error(
    "Operation failed",
    exc_info=True
)
```

## Response Headers

1. **Pagination Headers**:
```python
response.headers.update({
    "X-Total-Count": str(total_count),
    "X-Total-Pages": str(total_pages),
    "X-Current-Page": str(page),
    "X-Page-Size": str(page_size)
})
```

2. **Header Guidelines**:
   - Use X-prefix for custom headers
   - Convert all values to strings
   - Document header purposes in endpoint description

## Code Style

1. **Naming**:
   - Use descriptive variable names
   - Follow Python naming conventions
   - Use auxiliary verbs for boolean variables (is_, has_, etc.)

2. **Comments**:
   - Use section headers for clarity
   - Comment complex business logic
   - Keep comments up to date

3. **Error Handling**:
   - Use early returns for error conditions
   - Group related error checks
   - Provide context in error messages

## Refactoring Checklist

When cleaning up a router:
1. [ ] Move generic utilities to `utils/`
2. [ ] Organize code following the standard structure
3. [ ] Apply consistent error handling using `handle_supabase_operation`
4. [ ] Update documentation to follow standard format
5. [ ] Add appropriate logging at each level
6. [ ] Group endpoints in CRUD order
7. [ ] Review and update response headers
8. [ ] Check naming conventions and comments 