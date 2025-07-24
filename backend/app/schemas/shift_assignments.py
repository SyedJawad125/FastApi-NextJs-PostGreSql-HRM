from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime


# ✅ Base schema used in create/update
class ShiftAssignmentBase(BaseModel):
    employee_id: int
    shift_id: int
    date: date


# ✅ Create input schema
class ShiftAssignmentCreate(ShiftAssignmentBase):
    class Config:
        extra = "forbid"


# ✅ Update input schema
class ShiftAssignmentUpdate(BaseModel):
    employee_id: Optional[int] = None
    shift_id: Optional[int] = None
    date: Optional[date] = None

    class Config:
        extra = "forbid"


# ✅ Outgoing response schema (used in lists, single response)
class ShiftAssignmentOut(ShiftAssignmentBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }


# ✅ Paginated response schema
class PaginatedShiftAssignments(BaseModel):
    count: int
    data: List[ShiftAssignmentOut]

    model_config = {
        "from_attributes": True
    }


# ✅ Basic list response schema
class ShiftAssignmentListResponse(BaseModel):
    count: int
    data: List[ShiftAssignmentOut]

    model_config = {
        "from_attributes": True
    }
