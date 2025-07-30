from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

# Enum for feedback recommendation (matching your model)
class FeedbackRecommendation(str, Enum):
    strong_yes = "strong_yes"
    yes = "yes"
    neutral = "neutral"
    no = "no"
    strong_no = "strong_no"

# Optional: Nested schemas for relationships
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class InterviewOut(BaseModel):
    id: int
    # Add other interview fields as needed based on your Interview model

    class Config:
        from_attributes = True


# ✅ Base schema (shared fields)
class InterviewFeedbackBase(BaseModel):
    interview_id: int
    panel_member_id: Optional[int] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    overall_comment: str
    rating: Optional[int] = Field(None, ge=1, le=10)  # Assuming rating is 1-10 scale
    recommendation: FeedbackRecommendation = FeedbackRecommendation.neutral
    is_final: bool = False


# ✅ Create schema
class InterviewFeedbackCreate(InterviewFeedbackBase):
    pass


# ✅ Update schema
class InterviewFeedbackUpdate(BaseModel):
    interview_id: Optional[int] = None
    panel_member_id: Optional[int] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    overall_comment: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=10)
    recommendation: Optional[FeedbackRecommendation] = None
    is_final: Optional[bool] = None


# ✅ Response schema
class InterviewFeedbackOut(InterviewFeedbackBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int] = None
    submitted_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    # Optional nested output
    interview: Optional[InterviewOut] = None
    panel_member: Optional[UserOut] = None
    creator: Optional[UserOut] = None
    updater: Optional[UserOut] = None

    class Config:
        from_attributes = True


# ✅ Paginated response
class PaginatedInterviewFeedbacks(BaseModel):
    count: int
    data: List[InterviewFeedbackOut]


# ✅ Top-level response
class InterviewFeedbackListResponse(BaseModel):
    status: str
    result: PaginatedInterviewFeedbacks