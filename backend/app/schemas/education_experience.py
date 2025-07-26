from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date, datetime


class EducationExperienceBase(BaseModel):
    employee_id: int
    institution_name: str = Field(..., max_length=255)
    degree: str = Field(..., max_length=100)
    field_of_study: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    grade: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class EducationExperienceCreate(EducationExperienceBase):
    pass  # created_by_user_id handled internally


class EducationExperienceUpdate(BaseModel):
    institution_name: Optional[str] = Field(None, max_length=255)
    degree: Optional[str] = Field(None, max_length=100)
    field_of_study: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    grade: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class EducationExperienceOut(EducationExperienceBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PaginatedEducationExperiences(BaseModel):
    count: int
    data: List[EducationExperienceOut]


class EducationExperienceListResponse(BaseModel):
    status: str
    result: PaginatedEducationExperiences
