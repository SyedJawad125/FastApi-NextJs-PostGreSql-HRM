# models/performance_reviews.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, DateTime, CheckConstraint, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class PerformanceReview(Base):
    """Stores performance review records for employees."""
    __tablename__ = "performance_reviews"
    
    __table_args__ = (
        # Rating must be between 1 and 5
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
        # Review date cannot be in the future
        CheckConstraint('review_date <= CURRENT_DATE', name='check_review_date'),
        # Comments must be at least 10 characters if provided
        CheckConstraint('comments IS NULL OR LENGTH(comments) >= 10', name='check_comment_length'),
    )

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    reviewer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    review_date = Column(Date, nullable=False, index=True)
    rating = Column(Integer, nullable=False, default=3, index=True)
    comments = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    # Relationships
    employee = relationship("Employee", back_populates="performance_reviews")

    reviewer = relationship(
        "User",
        foreign_keys=[reviewer_id],
        back_populates="reviews_given"
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by_user_id],
        back_populates="created_reviews"
    )

    updater = relationship(
        "User",
        foreign_keys=[updated_by_user_id],
        back_populates="updated_reviews"
    )