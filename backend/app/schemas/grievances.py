from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


# === Enums ===

class GrievanceStatus(str, Enum):
    pending = "pending"
    under_review = "under_review"
    in_progress = "in_progress"
    resolved = "resolved"
    rejected = "rejected"
    closed = "closed"


# === Nested Schemas ===

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class EmployeeOut(BaseModel):
    id: int
    name: str  # Adjust as needed

    class Config:
        from_attributes = True


class DepartmentOut(BaseModel):
    id: int
    name: str  # Adjust as needed

    class Config:
        from_attributes = True


# === Base Schema ===

class GrievanceBase(BaseModel):
    employee_id: int
    dept_id: Optional[int] = None
    subject: str
    description: str
    status: GrievanceStatus = GrievanceStatus.pending


# === Create Schema (used for POST) ===

class GrievanceCreate(GrievanceBase):
    pass


# === Update Schema (used for PATCH) ===

class GrievanceUpdate(BaseModel):
    employee_id: Optional[int] = None
    dept_id: Optional[int] = None
    subject: Optional[str] = None
    description: Optional[str] = None
    status: Optional[GrievanceStatus] = None
    resolved_at: Optional[datetime] = None


# === Output Schema (used for GET) ===

class GrievanceOut(GrievanceBase):
    id: int
    submitted_at: datetime
    updated_at: Optional[datetime]
    resolved_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_by: Optional[int]
    created_by: Optional[int]

    # Optional nested relations
    employee: Optional[EmployeeOut]
    department: Optional[DepartmentOut]
    creator: Optional[UserOut]
    updater: Optional[UserOut]

    class Config:
        from_attributes = True


# === Paginated Response ===

class PaginatedGrievance(BaseModel):
    count: int
    data: List[GrievanceOut]


# === Top-level List Response ===

class GrievanceListResponse(BaseModel):
    status: str
    result: PaginatedGrievance
