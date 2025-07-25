from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


# Shared fields
class TrainingParticipantBase(BaseModel):
    training_id: int
    employee_id: int

    class Config:
        from_attributes = True


# POST payload
class TrainingParticipantCreate(TrainingParticipantBase):
    pass  # Exclude created_by_user_id and updated_by_user_id


# PATCH payload
class TrainingParticipantUpdate(BaseModel):
    training_id: Optional[int] = None
    employee_id: Optional[int] = None

    class Config:
        from_attributes = True


# Response schema
class TrainingParticipantOut(TrainingParticipantBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Paginated result
class PaginatedTrainingParticipants(BaseModel):
    count: int
    data: list[TrainingParticipantOut]


class TrainingParticipantListResponse(BaseModel):
    status: str
    result: PaginatedTrainingParticipants
