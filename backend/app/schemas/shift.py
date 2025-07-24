from pydantic import BaseModel
from typing import Optional, List
from datetime import time, datetime

# ✅ Shared fields
class ShiftBase(BaseModel):
    name: str
    start_time: time
    end_time: time
    break_minutes: Optional[int] = 0
    grace_period_minutes: Optional[int] = 0  # ✅ Newly added
    


# ✅ For creating a new shift
class ShiftCreate(ShiftBase):
    class Config:
        extra = "forbid"


# ✅ For updating an existing shift
class ShiftUpdate(BaseModel):
    name: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    break_minutes: Optional[int] = None
    grace_period_minutes: Optional[int] = None  # ✅ Newly added
    

    class Config:
        extra = "forbid"


# ✅ Outgoing single shift response
class ShiftOut(ShiftBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True  # For Pydantic v2 compatibility with ORM
    }


# ✅ Paginated list of shifts
class PaginatedShifts(BaseModel):
    count: int
    data: List[ShiftOut]

    model_config = {
        "from_attributes": True
    }


# ✅ Simple list of shifts
class ShiftListResponse(BaseModel):
    count: int
    data: List[ShiftOut]

    model_config = {
        "from_attributes": True
    }
