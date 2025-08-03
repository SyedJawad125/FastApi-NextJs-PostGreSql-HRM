# from pydantic import BaseModel, Field
# from typing import Optional, List
# from datetime import date, datetime


# # ✅ Nested output schemas
# class UserOut(BaseModel):
#     id: int
#     username: str

#     class Config:
#         from_attributes = True


# class EmployeeOut(BaseModel):
#     id: int
#     name: str

#     class Config:
#         from_attributes = True


# class DepartmentOut(BaseModel):
#     id: int
#     name: str

#     class Config:
#         from_attributes = True


# # ✅ Base schema (shared fields)
# class EmployeeLoanBase(BaseModel):
#     amount: float
#     loan_type: str
#     description: Optional[str] = None
#     issue_date: Optional[date] = None
#     due_date: Optional[date] = None
#     # status: Optional[str] = "pending"


# # ✅ Create schema
# class EmployeeLoanCreate(EmployeeLoanBase):
#     employee_id: int
#     department_id: int


# # ✅ Update schema
# class EmployeeLoanUpdate(BaseModel):
#     amount: Optional[float] = None
#     loan_type: Optional[str] = None
#     description: Optional[str] = None
#     issue_date: Optional[date] = None
#     due_date: Optional[date] = None
#     # status: Optional[str] = None
#     employee_id: Optional[int] = None
#     department_id: Optional[int] = None


# # ✅ Output schema (full response)
# class EmployeeLoanOut(EmployeeLoanBase):
#     id: int
#     employee_id: int
#     department_id: int

#     status: str  # ✅ Add this line explicitly

#     created_by_user_id: Optional[int]
#     updated_by_user_id: Optional[int]
#     approved_by_user_id: Optional[int]

#     created_at: Optional[datetime]
#     updated_at: Optional[datetime]

#     # Relationships
#     employee: Optional[EmployeeOut] = None
#     department: Optional[DepartmentOut] = None
#     creator: Optional[UserOut] = None
#     updater: Optional[UserOut] = None
#     approved_by: Optional[UserOut] = None   # ✅ match the model name

#     class Config:
#         from_attributes = True

# class LoanApprovalResponse(BaseModel):
#     id: int
#     status: str
#     approved_by_user_id: Optional[int]
#     approved_at: Optional[datetime]

#     class Config:
#         from_attributes = True


# # ✅ Paginated response wrapper
# class PaginatedEmployeeLoan(BaseModel):
#     count: int
#     data: List[EmployeeLoanOut]


# # ✅ Top-level response
# class EmployeeLoanListResponse(BaseModel):
#     status: str
#     result: PaginatedEmployeeLoan





from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
from decimal import Decimal

# ✅ Nested output schemas
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: Optional[str] = None

class EmployeeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    email: Optional[str] = None
    user_id: Optional[int] = None
    department_id: Optional[int] = None

class DepartmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str

# ✅ Enums for status and loan type
class LoanStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class LoanType(str, Enum):
    PERSONAL = "personal"
    EDUCATIONAL = "educational"
    MEDICAL = "medical"
    EMERGENCY = "emergency"
    ADVANCE = "advance"
    OTHER = "other"

# ✅ Base schema (shared fields)
class EmployeeLoanBase(BaseModel):
    amount: float = Field(..., gt=0, le=1000000, description="Loan amount (must be positive)")
    loan_type: LoanType = Field(..., description="Type of loan")
    description: str = Field(..., min_length=10, max_length=2000, description="Loan description/reason")
    issue_date: Optional[date] = Field(default=None, description="Date when loan was issued")
    due_date: Optional[date] = Field(default=None, description="Due date for loan repayment")
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError('Description cannot be empty')
        return v.strip()
    
    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v: Optional[date], info) -> Optional[date]:
        if v and info.data.get('issue_date') and v <= info.data['issue_date']:
            raise ValueError('Due date must be after issue date')
        return v

# ✅ Create schema (payload) - for regular users
class EmployeeLoanCreate(EmployeeLoanBase):
    department_id: int = Field(..., ge=1, description="Valid department ID")
    
    @field_validator('department_id')
    @classmethod
    def validate_department_id(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Department ID must be a positive integer.")
        return v

# ✅ Update schema (payload) - for regular users
class EmployeeLoanUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0, le=1000000)
    loan_type: Optional[LoanType] = None
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or v.strip() == ""):
            raise ValueError('Description cannot be empty')
        return v.strip() if v else v

# ✅ Admin update schema
class EmployeeLoanAdminUpdate(BaseModel):
    status: Optional[LoanStatus] = None
    amount: Optional[float] = Field(None, gt=0, le=1000000)
    loan_type: Optional[LoanType] = None
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    approved_by_user_id: Optional[int] = None
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or v.strip() == ""):
            raise ValueError('Description cannot be empty')
        return v.strip() if v else v

# ✅ Admin create schema
class EmployeeLoanAdminCreate(BaseModel):
    employee_id: int = Field(..., ge=1, description="Employee ID")
    department_id: int = Field(..., ge=1, description="Department ID")
    amount: float = Field(..., gt=0, le=1000000, description="Loan amount")
    loan_type: LoanType = Field(..., description="Type of loan")
    description: str = Field(..., min_length=10, max_length=2000, description="Loan description")
    issue_date: Optional[date] = Field(default=None, description="Issue date")
    due_date: Optional[date] = Field(default=None, description="Due date")
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError('Description cannot be empty')
        return v.strip()

# ✅ Admin patch schema
class EmployeeLoanAdminPatch(BaseModel):
    employee_id: Optional[int] = Field(None, ge=1, description="Employee ID")
    department_id: Optional[int] = Field(None, ge=1, description="Department ID")
    amount: Optional[float] = Field(None, gt=0, le=1000000, description="Loan amount")
    loan_type: Optional[LoanType] = None
    description: Optional[str] = Field(None, min_length=10, max_length=2000, description="Loan description")
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[LoanStatus] = Field(None, description="Loan status")  # ✅ Add this
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or v.strip() == ""):
            raise ValueError('Description cannot be empty')
        return v.strip() if v else v

# ✅ Output schema
class EmployeeLoanOut(EmployeeLoanBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    employee_id: int
    department_id: int
    status: LoanStatus
    request_user_id: Optional[int]  # <-- Make this Optional

    approved_by_user_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    
    date_requested: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Relationships
    employee: Optional[EmployeeOut] = None
    department: Optional[DepartmentOut] = None
    request_user: Optional[UserOut] = None
    approved_by: Optional[UserOut] = None
    creator: Optional[UserOut] = None
    updater: Optional[UserOut] = None

# ✅ Detailed output schema
class EmployeeLoanDetailOut(EmployeeLoanOut):
    can_edit: bool = Field(default=False, description="Whether current user can edit this loan")
    can_approve: bool = Field(default=False, description="Whether current user can approve this loan")
    is_owner: bool = Field(default=False, description="Whether current user owns this loan")

# ✅ Paginated wrapper
class PaginatedEmployeeLoan(BaseModel):
    count: int
    data: List[EmployeeLoanOut]
    page: Optional[int] = None
    page_size: Optional[int] = None
    total_pages: Optional[int] = None

class EmployeeLoanListResponse(BaseModel):
    status: str = "SUCCESSFUL"
    result: PaginatedEmployeeLoan

# ✅ Response schemas
class EmployeeLoanCreateResponse(BaseModel):
    status: str = "SUCCESSFUL"
    message: str = "Employee loan request created successfully"
    data: EmployeeLoanOut

class EmployeeLoanUpdateResponse(BaseModel):
    status: str = "SUCCESSFUL"
    message: str = "Employee loan request updated successfully"
    data: EmployeeLoanOut

# ✅ Delete response schema
class EmployeeLoanDeleteResponse(BaseModel):
    status: str = "SUCCESSFUL"
    message: str = "Employee loan request deleted successfully"

# ✅ Statistics schema
class EmployeeLoanStats(BaseModel):
    total_loans: int
    pending_loans: int
    approved_loans: int
    rejected_loans: int
    total_amount_requested: float
    total_amount_approved: float
    average_loan_amount: float