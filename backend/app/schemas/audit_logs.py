from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas.user import UserOut  # Ensure this is defined correctly


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    employee_id: Optional[int] = None  # ✅ Now accepts null values
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AuditLogBase(BaseModel):
    action: Optional[str] = Field(None, max_length=50)
    table_name: Optional[str] = None
    record_id: Optional[int] = None
    description: Optional[str] = None
    performed_by_user_id: Optional[int] = None
    # Do not include logged_by_user_id in the base; it's set internally.


class AuditLogCreate(AuditLogBase):
    pass  # logged_by_user_id will be injected server-side


class AuditLogUpdate(AuditLogBase):
    pass


class AuditLogOut(AuditLogBase):
    id: int
    created_by_user_id: int
    updated_by_user_id: Optional[int] = None
    logged_by_user_id: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    # ✅ Relationships
    performed_by: Optional[UserOut] = None
    logged_by: Optional[UserOut] = None

    class Config:
        from_attributes = True


class PaginatedAuditLogs(BaseModel):
    count: int
    data: List[AuditLogOut]


class AuditLogListResponse(BaseModel):
    status: str
    result: PaginatedAuditLogs
