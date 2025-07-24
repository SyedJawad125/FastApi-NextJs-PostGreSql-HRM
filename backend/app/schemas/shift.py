from ast import List
from pydantic import BaseModel
from typing import Optional
from datetime import time, datetime

from app.models.shift import Shift


class ShiftBase(BaseModel):
    name: str
    start_time: time
    end_time: time
    break_minutes: Optional[int] = 0
    description: Optional[str] = None


class ShiftCreate(ShiftBase):
    class Config:
        extra = "forbid"


class ShiftUpdate(BaseModel):
    name: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    break_minutes: Optional[int] = None
    description: Optional[str] = None

    class Config:
        extra = "forbid"


# ✅ Outgoing response model
class ShiftOut(ShiftBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class PaginatedShifts(BaseModel):
    count: int
    data: List[Shift]

class ShiftListResponse(BaseModel):
    count: int
    data: List[Shift]
