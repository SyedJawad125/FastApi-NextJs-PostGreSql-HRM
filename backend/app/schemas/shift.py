from pydantic import BaseModel
from typing import Optional, List
from datetime import time, datetime


# ✅ Shared base
class ShiftBase(BaseModel):
    name: str
    start_time: time
    end_time: time
    break_minutes: Optional[int] = 0
    grace_period_minutes: Optional[int] = 0


# ✅ Create schema (no created_by_user_id)
class ShiftCreate(ShiftBase):
    class Config:
        extra = "forbid"


# ✅ Update schema (no updated_by_user_id)
class ShiftUpdate(BaseModel):
    name: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    break_minutes: Optional[int] = None
    grace_period_minutes: Optional[int] = None

    class Config:
        extra = "forbid"


# ✅ Response schema (includes created_by, updated_by, timestamps)
class ShiftOut(ShiftBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }


# ✅ For paginated responses
class PaginatedShifts(BaseModel):
    count: int
    data: List[ShiftOut]

    model_config = {
        "from_attributes": True
    }


# ✅ Simple list response
class ShiftListResponse(BaseModel):
    count: int
    data: List[ShiftOut]

    model_config = {
        "from_attributes": True
    }
