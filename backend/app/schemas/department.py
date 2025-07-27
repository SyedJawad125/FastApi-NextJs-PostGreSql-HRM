from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# ✅ Base schema
class DepartmentBase(BaseModel):
    name: str
    location: Optional[str] = None

    class Config:
        from_attributes = True


# ✅ Payload for creating department (NO creator/updater in request)
class DepartmentCreate(DepartmentBase):
    pass  # No need to add created_by_user_id or updated_by_user_id

    class Config:
        extra = "forbid"


# ✅ Payload for updating department (PATCH)
class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

    class Config:
        extra = "forbid"
        from_attributes = True


# ✅ Response schema (includes creator/updater IDs)
class Department(DepartmentBase):
    id: int
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ✅ For paginated list responses
class PaginatedDepartments(BaseModel):
    count: int
    data: List[Department]


# ✅ Standardized response format
class DepartmentListResponse(BaseModel):
    status: str
    result: PaginatedDepartments
