from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


# ✅ Nested output schemas
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class EmployeeOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class DepartmentOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# ✅ Base schema (shared fields)
class EmployeeLoanBase(BaseModel):
    amount: float
    loan_type: str
    description: Optional[str] = None
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    # status: Optional[str] = "pending"


# ✅ Create schema
class EmployeeLoanCreate(EmployeeLoanBase):
    employee_id: int
    department_id: int


# ✅ Update schema
class EmployeeLoanUpdate(BaseModel):
    amount: Optional[float] = None
    loan_type: Optional[str] = None
    description: Optional[str] = None
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    # status: Optional[str] = None
    employee_id: Optional[int] = None
    department_id: Optional[int] = None


# ✅ Output schema (full response)
class EmployeeLoanOut(EmployeeLoanBase):
    id: int
    employee_id: int
    department_id: int

    status: str  # ✅ Add this line explicitly

    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    approved_by_user_id: Optional[int]

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    # Relationships
    employee: Optional[EmployeeOut] = None
    department: Optional[DepartmentOut] = None
    creator: Optional[UserOut] = None
    updater: Optional[UserOut] = None
    approved_by: Optional[UserOut] = None   # ✅ match the model name

    class Config:
        from_attributes = True

class LoanApprovalResponse(BaseModel):
    id: int
    status: str
    approved_by_user_id: Optional[int]
    approved_at: Optional[datetime]

    class Config:
        from_attributes = True


# ✅ Paginated response wrapper
class PaginatedEmployeeLoan(BaseModel):
    count: int
    data: List[EmployeeLoanOut]


# ✅ Top-level response
class EmployeeLoanListResponse(BaseModel):
    status: str
    result: PaginatedEmployeeLoan
