from typing import Optional
from pydantic import BaseModel, Field
from datetime import date


class RecruitmentBase(BaseModel):
    job_title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    posted_date: Optional[date] = None
    deadline: Optional[date] = None
    department_id: Optional[int] = None


class RecruitmentCreate(RecruitmentBase):
    pass  # server will set created_by, updated_by


class RecruitmentUpdate(RecruitmentBase):
    pass


class RecruitmentOut(RecruitmentBase):
    id: int
    created_by_user_id: int
    updated_by_user_id: Optional[int] = None

    class Config:
        from_attributes = True


class PaginatedRecruitments(BaseModel):
    count: int
    data: list[RecruitmentOut]


class RecruitmentListResponse(BaseModel):
    status: str
    result: PaginatedRecruitments
