from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date, datetime


# ✅ Base schema (shared fields, used for Create & Update)
class HealthCheckUpBase(BaseModel):
    employee_id: int
    department_id: int
    checkup_date: date
    blood_pressure: Optional[str] = Field(None, max_length=20)
    heart_rate: Optional[str] = Field(None, max_length=10)
    diagnosis: Optional[str] = Field(None, max_length=255)
    remarks: Optional[str] = Field(None, max_length=255)


# ✅ Create schema (input only, excludes audit info)
class HealthCheckUpCreate(HealthCheckUpBase):
    pass


# ✅ Update schema (all fields optional for PATCH-like behavior)
class HealthCheckUpUpdate(BaseModel):
    employee_id: Optional[int] = None
    department_id: Optional[int] = None
    checkup_date: Optional[date] = None
    blood_pressure: Optional[str] = Field(None, max_length=20)
    heart_rate: Optional[str] = Field(None, max_length=10)
    diagnosis: Optional[str] = Field(None, max_length=255)
    remarks: Optional[str] = Field(None, max_length=255)


# ✅ Response schema (includes audit/user info)
class HealthCheckUpOut(HealthCheckUpBase):
    id: int
    created_by_user_id: int
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # or orm_mode = True (for Pydantic v1)


# ✅ For paginated responses
class PaginatedHealthCheckUps(BaseModel):
    count: int
    data: List[HealthCheckUpOut]


# ✅ Top-level API response
class HealthCheckUpListResponse(BaseModel):
    status: str
    result: PaginatedHealthCheckUps
