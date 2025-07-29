from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# ✅ Nested User schema
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

# ✅ Base schema
class CompanyAnnouncementBase(BaseModel):
    title: str
    content: str
    is_active: Optional[bool] = True

# ✅ Create schema
class CompanyAnnouncementCreate(CompanyAnnouncementBase):
    pass

# ✅ Update schema (partial)
class CompanyAnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None

# ✅ Output schema with metadata and nested users
class CompanyAnnouncementOut(CompanyAnnouncementBase):
    id: int
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    creator: Optional[UserOut] = None
    updater: Optional[UserOut] = None

    class Config:
        from_attributes = True

# ✅ Paginated response
class PaginatedCompanyAnnouncements(BaseModel):
    count: int
    data: List[CompanyAnnouncementOut]

# ✅ List response wrapper
class CompanyAnnouncementListResponse(BaseModel):
    status: str
    result: PaginatedCompanyAnnouncements
