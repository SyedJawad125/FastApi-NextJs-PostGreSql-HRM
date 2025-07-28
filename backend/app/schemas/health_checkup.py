from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date, datetime

# Optional: Nested schemas for relationships
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class EmployeeOut(BaseModel):
    id: int
    name: str  # Adjust according to your Employee model

    class Config:
        from_attributes = True

class DepartmentOut(BaseModel):
    id: int
    name: str  # Adjust according to your Department model

    class Config:
        from_attributes = True


# ✅ Base schema (shared fields)
class HealthCheckUpBase(BaseModel):
    employee_id: int
    department_id: int
    checkup_date: date
    blood_pressure: Optional[str] = Field(None, max_length=20)
    heart_rate: Optional[str] = Field(None, max_length=10)
    diagnosis: Optional[str] = Field(None, max_length=255)
    remarks: Optional[str] = Field(None, max_length=255)


# ✅ Create schema
class HealthCheckUpCreate(HealthCheckUpBase):
    pass


# ✅ Update schema
class HealthCheckUpUpdate(BaseModel):
    employee_id: Optional[int] = None
    department_id: Optional[int] = None
    checkup_date: Optional[date] = None
    blood_pressure: Optional[str] = Field(None, max_length=20)
    heart_rate: Optional[str] = Field(None, max_length=10)
    diagnosis: Optional[str] = Field(None, max_length=255)
    remarks: Optional[str] = Field(None, max_length=255)


# ✅ Response schema
class HealthCheckUpOut(HealthCheckUpBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    # Optional nested output
    employee: Optional[EmployeeOut] = None
    department: Optional[DepartmentOut] = None
    creator: Optional[UserOut] = None
    updater: Optional[UserOut] = None

    class Config:
        from_attributes = True


# ✅ Paginated response
class PaginatedHealthCheckUps(BaseModel):
    count: int
    data: List[HealthCheckUpOut]


# ✅ Top-level response
class HealthCheckUpListResponse(BaseModel):
    status: str
    result: PaginatedHealthCheckUps
