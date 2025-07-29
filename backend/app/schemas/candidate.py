# from typing import Optional
# from pydantic import BaseModel, Field
# from datetime import date, datetime


# class CandidateBase(BaseModel):
#     name: Optional[str] = Field(None, max_length=100)
#     email: Optional[str] = Field(None)
#     phone: Optional[str] = Field(None)
#     resume: Optional[str] = None  # URL or file path
#     applied_date: Optional[date] = None
#     recruitment_id: Optional[int] = None


# class CandidateCreate(CandidateBase):
#     pass  # All required fields are set by the server or optional


# class CandidateUpdate(CandidateBase):
#     pass


# class CandidateOut(CandidateBase):
#     id: int
#     created_by_user_id: int
#     updated_by_user_id: Optional[int] = None
#     created_at: Optional[datetime]
#     updated_at: Optional[datetime]

#     class Config:
#         from_attributes = True


# class PaginatedCandidates(BaseModel):
#     count: int
#     data: list[CandidateOut]


# class CandidateListResponse(BaseModel):
#     status: str
#     result: PaginatedCandidates



from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date, datetime


class CandidateBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    resume: Optional[str] = None  # File path or URL
    resume_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    skills: Optional[str] = None  # Can be a JSON string or comma-separated
    experience_years: Optional[int] = 0
    education: Optional[str] = None
    is_available: Optional[bool] = True
    applied_date: Optional[date] = None
    recruitment_id: Optional[int] = None
    user_id: Optional[int] = None


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(CandidateBase):
    pass


class CandidateOut(CandidateBase):
    id: int
    created_by_user_id: int
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PaginatedCandidates(BaseModel):
    count: int
    data: List[CandidateOut]


class CandidateListResponse(BaseModel):
    status: str
    result: PaginatedCandidates
