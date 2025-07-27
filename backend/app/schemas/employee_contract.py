from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


# ✅ Base schema used for shared fields
class EmployeeContractBase(BaseModel):
    employee_id: int
    department_id: Optional[int] = None
    contract_type: str = Field(..., max_length=100)
    start_date: date
    end_date: Optional[date] = None
    salary: float
    description: str


# ✅ Schema for creating a new employee contract (no audit fields)
class EmployeeContractCreate(EmployeeContractBase):
    pass


# ✅ Schema for updating an employee contract (no audit fields)
class EmployeeContractUpdate(EmployeeContractBase):
    pass


# ✅ Schema for reading contract (include audit fields)
class EmployeeContractOut(EmployeeContractBase):
    id: int
    created_by_user_id: int
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # ✅ Allows ORM -> schema conversion


# ✅ Paginated output schema (optional)
class PaginatedEmployeeContracts(BaseModel):
    count: int
    data: list[EmployeeContractOut]


# ✅ General API response wrapper (optional)
class EmployeeContractListResponse(BaseModel):
    status: str
    result: PaginatedEmployeeContracts
