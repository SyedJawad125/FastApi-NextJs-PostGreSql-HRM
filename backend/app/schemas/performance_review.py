from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime


class PerformanceReviewBase(BaseModel):
    employee_id: Optional[int] = Field(None, description="ID of the reviewed employee")
    reviewer_id: Optional[int] = Field(None, description="User ID of the reviewer")
    review_date: Optional[date] = Field(None, description="Date of the review")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1 to 5")
    comments: Optional[str] = Field(None, min_length=10, description="Optional comments with a minimum of 10 characters")


class PerformanceReviewCreate(PerformanceReviewBase):
    employee_id: int
    review_date: date
    rating: int


class PerformanceReviewUpdate(PerformanceReviewBase):
    pass


class PerformanceReviewOut(PerformanceReviewBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PaginatedPerformanceReviews(BaseModel):
    count: int
    data: list[PerformanceReviewOut]


class PerformanceReviewListResponse(BaseModel):
    status: str
    result: PaginatedPerformanceReviews
