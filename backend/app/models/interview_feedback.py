# models/interview_feedback.py

from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Boolean, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

# Enum for feedback recommendation
class FeedbackRecommendation(enum.Enum):
    strong_yes = "strong_yes"
    yes = "yes"
    neutral = "neutral"
    no = "no"
    strong_no = "strong_no"

class InterviewFeedback(Base):
    __tablename__ = "interview_feedbacks"

    id = Column(Integer, primary_key=True, index=True)

    # === Foreign Keys ===
    interview_id = Column(Integer, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False)
    panel_member_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    # === Feedback Attributes ===
    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)
    overall_comment = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)
    recommendation = Column(SqlEnum(FeedbackRecommendation), nullable=False, default=FeedbackRecommendation.neutral)

    is_final = Column(Boolean, default=False)

    # === Timestamps ===
    submitted_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # === Relationships ===
    interview = relationship("Interview", back_populates="interview_feedbacks")
    panel_member = relationship("User", foreign_keys=[panel_member_id], back_populates="interview_feedbacks")
    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_interview_feedbacks")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_interview_feedbacks")
