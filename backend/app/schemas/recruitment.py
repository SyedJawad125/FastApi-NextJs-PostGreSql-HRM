# from typing import Optional
# from pydantic import BaseModel, Field
# from datetime import date, datetime


# class RecruitmentBase(BaseModel):
#     job_title: Optional[str] = Field(None, max_length=100)
#     description: Optional[str] = Field(None, max_length=1000)
#     posted_date: Optional[date] = None
#     deadline: Optional[date] = None
#     department_id: Optional[int] = None


# class RecruitmentCreate(RecruitmentBase):
#     pass  # server will set created_by, updated_by


# class RecruitmentUpdate(RecruitmentBase):
#     pass


# class RecruitmentOut(RecruitmentBase):
#     id: int
#     created_by_user_id: int
#     updated_by_user_id: Optional[int] = None
#     created_at: Optional[datetime]
#     updated_at: Optional[datetime]

#     class Config:
#         from_attributes = True


# class PaginatedRecruitments(BaseModel):
#     count: int
#     data: list[RecruitmentOut]


# class RecruitmentListResponse(BaseModel):
#     status: str
#     result: PaginatedRecruitments





from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_serializer
from datetime import date, datetime
from enum import Enum
from decimal import Decimal

# === ENUMS ===
class JobType(str, Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    internship = "internship"
    freelance = "freelance"

class JobLevel(str, Enum):
    entry = "entry"
    junior = "junior"
    mid = "mid"
    senior = "senior"
    lead = "lead"
    manager = "manager"
    director = "director"
    executive = "executive"

class JobStatus(str, Enum):
    draft = "draft"
    active = "active"
    paused = "paused"
    closed = "closed"
    cancelled = "cancelled"

class WorkMode(str, Enum):
    onsite = "onsite"
    remote = "remote"
    hybrid = "hybrid"


# === BASE SCHEMA ===
class RecruitmentBase(BaseModel):
    job_title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None

    job_type: Optional[JobType] = JobType.full_time
    job_level: Optional[JobLevel] = JobLevel.mid
    work_mode: Optional[WorkMode] = WorkMode.onsite
    status: Optional[JobStatus] = JobStatus.draft

    location: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    salary_min: Optional[Decimal] = None
    salary_max: Optional[Decimal] = None
    currency: Optional[str] = "USD"

    min_experience_years: Optional[int] = 0
    max_experience_years: Optional[int] = None
    education_level: Optional[str] = None

    max_applicants: Optional[int] = None
    auto_close_when_full: Optional[bool] = False
    application_instructions: Optional[str] = None

    required_skills: Optional[str] = None
    preferred_skills: Optional[str] = None
    tags: Optional[str] = None

    posted_date: Optional[date] = None
    deadline: Optional[date] = None
    last_activity_date: Optional[date] = None

    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None

    is_urgent: Optional[bool] = False
    is_featured: Optional[bool] = False
    is_confidential: Optional[bool] = False
    allow_remote_candidates: Optional[bool] = True
    requires_visa_sponsorship: Optional[bool] = False

    slug: Optional[str] = None
    meta_description: Optional[str] = None
    external_job_boards: Optional[str] = None

    department_id: Optional[int] = None


# === CREATE / UPDATE SCHEMAS ===
class RecruitmentCreate(RecruitmentBase):
    pass

class RecruitmentUpdate(RecruitmentBase):
    pass


# === OUT SCHEMA ===
class RecruitmentOut(RecruitmentBase):
    id: int
    created_by_employee_id: Optional[int] = None
    hiring_manager_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    view_count: Optional[int] = 0
    application_count: Optional[int] = 0

    

    @field_serializer('salary_min', 'salary_max')
    def serialize_decimal(self, value: Decimal) -> float:
        return float(value) if value is not None else None

    class Config:
        from_attributes = True

# === PAGINATION WRAPPERS ===
class PaginatedRecruitments(BaseModel):
    count: int
    data: List[RecruitmentOut]

class RecruitmentListResponse(BaseModel):
    status: str
    result: PaginatedRecruitments
