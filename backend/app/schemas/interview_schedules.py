from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


# === Enums ===
class InterviewScheduleStatus(str, Enum):
    scheduled = "scheduled"
    rescheduled = "rescheduled"
    canceled = "canceled"
    completed = "completed"


# === Reusable UserOut (Same as your UserOut) ===
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# === Reusable InterviewMinimalOut (to avoid full loop) ===
class InterviewMinimalOut(BaseModel):
    id: int
    job_application_id: int

    class Config:
        from_attributes = True


# === Base Schema ===
class InterviewScheduleBase(BaseModel):
    interview_id: int
    scheduled_by_user_id: Optional[int] = None
    rescheduled_from_id: Optional[int] = None

    scheduled_datetime: datetime
    duration_minutes: Optional[int] = None
    time_zone: Optional[str] = "Asia/Karachi"
    mode: Optional[str] = "offline"  # online, offline, hybrid
    location: Optional[str] = None

    status: InterviewScheduleStatus = InterviewScheduleStatus.scheduled
    remarks: Optional[str] = None


# === Create Schema ===
class InterviewScheduleCreate(InterviewScheduleBase):
    created_by_user_id: Optional[int] = None


# === Update Schema ===
class InterviewScheduleUpdate(BaseModel):
    scheduled_datetime: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    time_zone: Optional[str] = None
    mode: Optional[str] = None
    location: Optional[str] = None
    status: Optional[InterviewScheduleStatus] = None
    remarks: Optional[str] = None
    updated_by_user_id: Optional[int] = None


# === Output Schema ===
class InterviewScheduleOut(InterviewScheduleBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None

    scheduler: Optional[UserOut] = None
    creator: Optional[UserOut] = None
    updater: Optional[UserOut] = None
    interview: Optional[InterviewMinimalOut] = None
    rescheduled_from: Optional['InterviewScheduleOut'] = None  # self-reference

    class Config:
        from_attributes = True


# For recursive self-reference
InterviewScheduleOut.update_forward_refs()


class PaginatedInterviewSchedules(BaseModel):
    count: int
    data: List["InterviewScheduleOut"]

    class Config:
        orm_mode = True


class InterviewScheduleListResponse(BaseModel):
    status: str
    result: PaginatedInterviewSchedules

    class Config:
        orm_mode = True