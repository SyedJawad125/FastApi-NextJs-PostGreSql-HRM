from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


# === Enums ===

class TravelExpenseStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    paid = "paid"
    cancelled = "cancelled"


# === Nested Schemas ===

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


# === Base Schema ===

class TravelExpenseBase(BaseModel):
    employee_id: int
    submitted_by_user_id: int
    approved_by_user_id: Optional[int] = None
    department_id: int
    purpose: str
    description: Optional[str] = None
    travel_date: datetime
    return_date: Optional[datetime] = None
    total_amount: float
    currency: Optional[str] = "USD"
    status: Optional[TravelExpenseStatus] = TravelExpenseStatus.pending


# === Create Schema (POST) ===

class TravelExpenseCreate(TravelExpenseBase):
    pass


# === Update Schema (PATCH) ===

class TravelExpenseUpdate(BaseModel):
    employee_id: Optional[int] = None
    submitted_by_user_id: Optional[int] = None
    approved_by_user_id: Optional[int] = None
    department_id: Optional[int] = None
    purpose: Optional[str] = None
    description: Optional[str] = None
    travel_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    status: Optional[TravelExpenseStatus] = None


# === Output Schema (GET) ===

class TravelExpenseOut(TravelExpenseBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]

    # Optional nested relations
    employee: Optional[EmployeeOut]
    department: Optional[DepartmentOut]
    creator: Optional[UserOut]
    updater: Optional[UserOut]
    submitter: Optional[UserOut]
    approver: Optional[UserOut]

    class Config:
        from_attributes = True


# === Paginated Response ===

class PaginatedTravelExpense(BaseModel):
    count: int
    data: List[TravelExpenseOut]


# === List Response ===

class TravelExpenseListResponse(BaseModel):
    status: str
    result: PaginatedTravelExpense
