from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class AuditLogBase(BaseModel):
    action: Optional[str] = Field(None, max_length=50)
    table_name: Optional[str] = None
    record_id: Optional[int] = None
    description: Optional[str] = None
    performed_by_user_id: Optional[int] = None
    logged_by_user_id: Optional[int] = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogUpdate(AuditLogBase):
    pass


class AuditLogOut(AuditLogBase):
    id: int
    created_by_user_id: int
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PaginatedAuditLogs(BaseModel):
    count: int
    data: list[AuditLogOut]


class AuditLogListResponse(BaseModel):
    status: str
    result: PaginatedAuditLogs
