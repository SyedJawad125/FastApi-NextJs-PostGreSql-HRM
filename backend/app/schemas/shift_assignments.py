from ast import List
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

from app.models.shift_assignments import ShiftAssignment


class ShiftAssignmentBase(BaseModel):
    employee_id: int
    shift_id: int
    date: date


class ShiftAssignmentCreate(ShiftAssignmentBase):
    class Config:
        extra = "forbid"


class ShiftAssignmentUpdate(BaseModel):
    employee_id: Optional[int] = None
    shift_id: Optional[int] = None
    date: Optional[date] = None

    class Config:
        extra = "forbid"


# ✅ Outgoing response model
class ShiftAssignmentOut(ShiftAssignmentBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class PaginatedShiftAssignments(BaseModel):
    count: int
    data: List[ShiftAssignment]

class ShiftAssignmentListResponse(BaseModel):
    count: int
    data: List[ShiftAssignment]
