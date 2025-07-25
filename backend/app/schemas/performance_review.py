from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime


class PerformanceReviewBase(BaseModel):
    employee_id: Optional[int] = Field(None, description="ID of the reviewed employee")
    reviewer_id: Optional[int] = Field(None, description="User ID of the reviewer (defaults to the creator if not specified)")
    review_date: Optional[date] = Field(None, description="Date of the review")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1 to 5")
    comments: Optional[str] = Field(None, min_length=10, description="Optional comments with a minimum of 10 characters")


class PerformanceReviewCreate(PerformanceReviewBase):
    employee_id: int = Field(..., description="Required ID of the employee being reviewed")
    review_date: date = Field(..., description="Required date of the review")
    rating: int = Field(..., ge=1, le=5, description="Required rating (1-5)")
    reviewer_id: Optional[int] = Field(None, description="Optional reviewer ID (defaults to the logged-in user)")


class PerformanceReviewUpdate(PerformanceReviewBase):
    pass


class PerformanceReviewOut(PerformanceReviewBase):
    id: int = Field(..., description="Unique ID of the performance review")
    reviewer_id: Optional[int] = Field(None, description="User ID of the reviewer (can be null)")
    created_by_user_id: int = Field(..., description="User ID who created the review")
    updated_by_user_id: Optional[int] = Field(None, description="User ID who last updated the review (null if never updated)")
    created_at: datetime = Field(..., description="Timestamp when the review was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the review was last updated (null if never updated)")

    class Config:
        from_attributes = True  # Enables ORM mode (formerly `orm_mode = True`)


class PaginatedPerformanceReviews(BaseModel):
    count: int = Field(..., description="Total number of reviews available")
    data: list[PerformanceReviewOut] = Field(..., description="List of performance reviews")


class PerformanceReviewListResponse(BaseModel):
    status: str = Field(..., example="success", description="API response status")
    result: PaginatedPerformanceReviews = Field(..., description="Paginated review data")