from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime

# ✅ Shared base schema
class ShiftAssignmentBase(BaseModel):
    employee_id: int
    shift_id: Optional[int]  # Because shift_id is nullable in the model
    date: date


# ✅ Create input schema (no audit fields allowed)
class ShiftAssignmentCreate(ShiftAssignmentBase):
    class Config:
        extra = "forbid"


# ✅ Update input schema (partial updates, no audit fields allowed)
class ShiftAssignmentUpdate(BaseModel):
    employee_id: Optional[int] = None
    shift_id: Optional[int] = None
    date: Optional[date] = None

    class Config:
        extra = "forbid"


# ✅ Output schema (includes audit fields and metadata)
class ShiftAssignmentOut(ShiftAssignmentBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }


# ✅ Paginated list response
class PaginatedShiftAssignments(BaseModel):
    count: int
    data: List[ShiftAssignmentOut]

    model_config = {
        "from_attributes": True
    }


# ✅ Standard list response
class ShiftAssignmentListResponse(BaseModel):
    count: int
    data: List[ShiftAssignmentOut]

    model_config = {
        "from_attributes": True
    }
