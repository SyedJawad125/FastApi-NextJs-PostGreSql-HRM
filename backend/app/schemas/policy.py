from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


# === Nested Schemas ===

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class DepartmentOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class PolicyAttachmentOut(BaseModel):
    id: int
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class PolicyAcknowledgementOut(BaseModel):
    id: int
    user_id: int
    acknowledged_at: datetime

    class Config:
        from_attributes = True


# === Base Schema ===

class PolicyBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    effective_date: datetime
    expiry_date: Optional[datetime] = None
    version: Optional[str] = "1.0"
    is_active: bool = True
    department_id: Optional[int] = None


# === Create Schema (used for POST) ===
# ⛔ removed created_by_user_id (will be set by backend)

class PolicyCreate(PolicyBase):
    pass


# === Update Schema (used for PATCH) ===
# ⛔ removed updated_by_user_id (will be set by backend)

class PolicyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    version: Optional[str] = None
    is_active: Optional[bool] = None
    department_id: Optional[int] = None


# === Output Schema (used for GET) ===

class PolicyOut(PolicyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Relations
    department: Optional[DepartmentOut]
    creator: Optional[UserOut]
    updater: Optional[UserOut]
    attachments: List[PolicyAttachmentOut] = []
    acknowledgements: List[PolicyAcknowledgementOut] = []

    class Config:
        from_attributes = True


# === Paginated Response ===

class PaginatedPolicy(BaseModel):
    count: int
    data: List[PolicyOut]


# === Top-level List Response ===

class PolicyListResponse(BaseModel):
    status: str
    result: PaginatedPolicy
