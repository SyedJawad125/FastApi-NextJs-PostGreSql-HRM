from pydantic import BaseModel
from typing import Optional, List
from datetime import date


# ---------------- Base Schema (Shared) ----------------
class HolidayCalendarBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: date
    is_optional: Optional[bool] = False
    is_national: Optional[bool] = True
    department_id: Optional[int] = None
    employee_ids: Optional[List[int]] = []  # For create/update only

    class Config:
        orm_mode = True


# ---------------- Create Schema ----------------
class HolidayCalendarCreate(HolidayCalendarBase):
    pass


# ---------------- Update Schema ----------------
class HolidayCalendarUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None 
    is_optional: Optional[bool] = None
    is_national: Optional[bool] = None
    department_id: Optional[int] = None
    employee_ids: Optional[List[int]] = None

    class Config:
        orm_mode = True


# ---------------- Response Schema ----------------
class HolidayCalendarOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    date: date
    is_optional: bool
    is_national: bool
    department_id: Optional[int]
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[date]
    updated_at: Optional[date]
    employees: Optional[List[int]] = []  # Returns list of employee IDs linked to the holiday

    class Config:
        orm_mode = True
