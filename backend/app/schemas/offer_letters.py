from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

# === Enums ===
class OfferStatusEnum(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

# === Reusable Related Schemas ===
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class CandidateBasicOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class JobApplicationBasicOut(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True

class RecruitmentBasicOut(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True

class InterviewBasicOut(BaseModel):
    id: int
    interview_datetime: datetime

    class Config:
        from_attributes = True

# === Base Schema ===
class OfferLetterBase(BaseModel):
    candidate_id: int
    job_application_id: int
    recruitment_id: int
    interview_id: Optional[int] = None

    job_title: str
    offer_date: Optional[date] = None
    joining_date: date
    salary_package: str
    benefits: Optional[str] = None
    status: OfferStatusEnum = OfferStatusEnum.pending
    issued_by: str
    offer_body: Optional[str] = None
    pdf_path: Optional[str] = None

# === Create Schema ===
class OfferLetterCreate(OfferLetterBase):
    pass

# === Update Schema ===
class OfferLetterUpdate(BaseModel):
    job_title: Optional[str] = None
    offer_date: Optional[date] = None
    joining_date: Optional[date] = None
    salary_package: Optional[str] = None
    benefits: Optional[str] = None
    status: Optional[OfferStatusEnum] = None
    issued_by: Optional[str] = None
    offer_body: Optional[str] = None
    pdf_path: Optional[str] = None
    interview_id: Optional[int] = None

# === Output Schema ===
class OfferLetterOut(OfferLetterBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]

    candidate: Optional[CandidateBasicOut]
    job_application: Optional[JobApplicationBasicOut]
    recruitment: Optional[RecruitmentBasicOut]
    interview: Optional[InterviewBasicOut]

    creator: Optional[UserOut]
    updater: Optional[UserOut]

    class Config:
        from_attributes = True

# === Paginated and List Response Wrappers ===
class PaginatedOfferLetters(BaseModel):
    count: int
    data: List[OfferLetterOut]

class OfferLetterListResponse(BaseModel):
    status: str
    result: PaginatedOfferLetters
