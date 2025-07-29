from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal
from enum import Enum


# === Enums ===
class ApplicationStatus(str, Enum):
    applied = "applied"
    reviewed = "reviewed"
    shortlisted = "shortlisted"
    rejected = "rejected"
    hired = "hired"


# === User Schema ===
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# === Candidate and Recruitment Placeholder (Optional) ===
class CandidateOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RecruitmentOut(BaseModel):
    id: int
    job_title: str

    class Config:
        from_attributes = True


# === Base Schema ===
class JobApplicationBase(BaseModel):
    candidate_id: int
    recruitment_id: int

    application_date: Optional[datetime] = None
    cover_letter: Optional[str] = None
    resume: Optional[str] = None

    status: Optional[ApplicationStatus] = ApplicationStatus.applied
    interview_date: Optional[datetime] = None
    interview_feedback: Optional[str] = None

    expected_salary: Optional[Decimal] = None
    current_salary: Optional[Decimal] = None
    notice_period_days: Optional[int] = None
    available_from: Optional[date] = None


# === Create Schema ===
class JobApplicationCreate(JobApplicationBase):
    pass


# === Update Schema ===
class JobApplicationUpdate(BaseModel):
    cover_letter: Optional[str] = None
    resume: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    interview_date: Optional[datetime] = None
    interview_feedback: Optional[str] = None
    expected_salary: Optional[Decimal] = None
    current_salary: Optional[Decimal] = None
    notice_period_days: Optional[int] = None
    available_from: Optional[date] = None


# === Output Schema ===
class JobApplicationOut(JobApplicationBase):
    id: int
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    creator: Optional[UserOut] = None
    updater: Optional[UserOut] = None

    candidate: Optional[CandidateOut] = None
    recruitment: Optional[RecruitmentOut] = None

    class Config:
        from_attributes = True


# === Paginated Output ===
class PaginatedJobApplications(BaseModel):
    count: int
    data: List[JobApplicationOut]


# === List Response Wrapper ===
class JobApplicationListResponse(BaseModel):
    status: str
    result: PaginatedJobApplications
