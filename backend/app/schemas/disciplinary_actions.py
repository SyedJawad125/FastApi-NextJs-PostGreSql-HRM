from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


# === Enum ===

class DisciplinaryActionStatus(str, Enum):
    pending = "pending"
    reviewed = "reviewed"
    action_taken = "action_taken"
    resolved = "resolved"
    closed = "closed"


# === Nested Schemas ===

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class EmployeeOut(BaseModel):
    id: int
    name: str  # adjust field as needed

    class Config:
        from_attributes = True


# === Base Schema ===

class DisciplinaryActionBase(BaseModel):
    employee_id: int
    reason: str
    action: Optional[str] = None
    status: Optional[DisciplinaryActionStatus] = DisciplinaryActionStatus.pending
    issued_by: str
    issued_date: Optional[datetime] = None


# === Create Schema (POST) ===

class DisciplinaryActionCreate(DisciplinaryActionBase):
    pass


# === Update Schema (PATCH) ===

class DisciplinaryActionUpdate(BaseModel):
    employee_id: Optional[int] = None
    reason: Optional[str] = None
    action: Optional[str] = None
    status: Optional[DisciplinaryActionStatus] = None
    issued_by: Optional[str] = None
    issued_date: Optional[datetime] = None


# === Output Schema (GET) ===

class DisciplinaryActionOut(DisciplinaryActionBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]

    employee: Optional[EmployeeOut]
    creator: Optional[UserOut]
    updater: Optional[UserOut]

    class Config:
        from_attributes = True


# === Paginated Response ===

class PaginatedDisciplinaryAction(BaseModel):
    count: int
    data: List[DisciplinaryActionOut]


# === Top-level List Response ===

class DisciplinaryActionListResponse(BaseModel):
    status: str
    result: PaginatedDisciplinaryAction
