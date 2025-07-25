from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime


# Base schema (shared fields)
class TrainingBase(BaseModel):
    employee_id: int
    trainer_id: Optional[int] = Field(None, description="Trainer user ID")
    department_id: Optional[int] = Field(None, description="Department ID")
    training_title: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    training_date: date

    class Config:
        from_attributes = True


# Payload for POST
class TrainingCreate(TrainingBase):
    pass  # No created_by_user_id or updated_by_user_id


# Payload for PATCH
class TrainingUpdate(BaseModel):
    employee_id: Optional[int] = None
    trainer_id: Optional[int] = None
    department_id: Optional[int] = None
    training_title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    training_date: Optional[date] = None

    class Config:
        from_attributes = True


# Response schema (GET/POST/PATCH output)
class TrainingOut(TrainingBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# For paginated listing
class PaginatedTrainings(BaseModel):
    count: int
    data: list[TrainingOut]


class TrainingListResponse(BaseModel):
    status: str
    result: PaginatedTrainings
