# schemas/interview.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


# === Enums ===
class InterviewMode(str, Enum):
    online = "online"
    offline = "offline"
    phone = "phone"


class InterviewStatus(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"


# === Related User Schema (reusable) ===
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# === Related JobApplication Schema (minimal) ===
class JobApplicationBasicOut(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True


# === Base Schema ===
class InterviewBase(BaseModel):
    job_application_id: int
    interviewer_id: int

    interview_datetime: datetime
    location: Optional[str] = None
    mode: Optional[InterviewMode] = InterviewMode.online
    status: Optional[InterviewStatus] = InterviewStatus.scheduled

    duration_minutes: Optional[int] = None
    feedback: Optional[str] = None
    remarks: Optional[str] = None


# === Create Schema ===
class InterviewCreate(InterviewBase):
    pass


# === Update Schema ===
class InterviewUpdate(BaseModel):
    interview_datetime: Optional[datetime] = None
    location: Optional[str] = None
    mode: Optional[InterviewMode] = None
    status: Optional[InterviewStatus] = None
    duration_minutes: Optional[int] = None
    feedback: Optional[str] = None
    remarks: Optional[str] = None


# === Output Schema ===
class InterviewOut(InterviewBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None

    job_application: Optional[JobApplicationBasicOut] = None
    interviewer: Optional[UserOut] = None
    creator: Optional[UserOut] = None
    updater: Optional[UserOut] = None

    class Config:
        from_attributes = True


# === Paginated and List Response Wrappers ===
class PaginatedInterviews(BaseModel):
    count: int
    data: List[InterviewOut]


class InterviewListResponse(BaseModel):
    status: str
    result: PaginatedInterviews
