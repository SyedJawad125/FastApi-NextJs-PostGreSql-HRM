from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date, datetime

# ✅ Nested output schemas
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

# ✅ Base schema for shared fields
class AdvancedSalaryBase(BaseModel):
    amount: float
    reason: Optional[str] = None
    request_date: date
    approved_date: Optional[date] = None
    status: Optional[str] = Field(default="pending")
    employee_id: int
    department_id: int

# ✅ Create schema (no created_by/updated_by fields)
class AdvancedSalaryCreate(AdvancedSalaryBase):
    pass

# ✅ Update schema (partial fields, no created_by/updated_by)
class AdvancedSalaryUpdate(BaseModel):
    amount: Optional[float] = None
    reason: Optional[str] = None
    request_date: Optional[date] = None
    approved_date: Optional[date] = None
    status: Optional[str] = None
    employee_id: Optional[int] = None
    department_id: Optional[int] = None

# ✅ Response schema with metadata and nested relations
class AdvancedSalaryOut(AdvancedSalaryBase):
    id: int
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Optional nested output
    employee: Optional[EmployeeOut] = None
    department: Optional[DepartmentOut] = None
    creator: Optional[UserOut] = None
    updater: Optional[UserOut] = None

    class Config:
        from_attributes = True

# ✅ Paginated response
class PaginatedAdvancedSalaries(BaseModel):
    count: int
    data: List[AdvancedSalaryOut]

# ✅ List response wrapper
class AdvancedSalaryListResponse(BaseModel):
    status: str
    result: PaginatedAdvancedSalaries
