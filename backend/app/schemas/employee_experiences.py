from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date, datetime


# --- Base Schema ---
class EmployeeExperienceBase(BaseModel):
    employee_id: int
    job_title: str = Field(..., max_length=100)
    company_name: str = Field(..., max_length=100)
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None


# --- Create Schema (input for single/multiple) ---
class EmployeeExperienceCreate(EmployeeExperienceBase):
    pass  # created_by_user_id is handled internally


# --- Update Schema (PATCH) ---
class EmployeeExperienceUpdate(BaseModel):
    job_title: Optional[str] = Field(None, max_length=100)
    company_name: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None


# --- Output Schema ---
class EmployeeExperienceOut(EmployeeExperienceBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# --- For pagination output ---
class PaginatedEmployeeExperiences(BaseModel):
    count: int
    data: List[EmployeeExperienceOut]


# --- Top-level response wrapper ---
class EmployeeExperienceListResponse(BaseModel):
    status: str
    result: PaginatedEmployeeExperiences
