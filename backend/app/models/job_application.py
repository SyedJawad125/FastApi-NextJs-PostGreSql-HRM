# models/job_application.py

from sqlalchemy import (
    Column, Integer, ForeignKey, DateTime, Text, Numeric, Enum as SqlEnum, Date
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class ApplicationStatus(enum.Enum):
    applied = "applied"
    reviewed = "reviewed"
    shortlisted = "shortlisted"
    rejected = "rejected"
    hired = "hired"

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    recruitment_id = Column(Integer, ForeignKey("recruitments.id"), nullable=False)

    application_date = Column(DateTime, default=datetime.utcnow)
    cover_letter = Column(Text, nullable=True)
    resume = Column(Text, nullable=True)

    status = Column(SqlEnum(ApplicationStatus), default=ApplicationStatus.applied)
    interview_date = Column(DateTime, nullable=True)
    interview_feedback = Column(Text, nullable=True)

    expected_salary = Column(Numeric(10, 2), nullable=True)
    current_salary = Column(Numeric(10, 2), nullable=True)
    notice_period_days = Column(Integer, nullable=True)
    available_from = Column(Date, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # User Tracking
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    candidate = relationship("Candidate", back_populates="job_applications")
    recruitment = relationship("Recruitment", back_populates="job_applications")
    interviews = relationship("Interview", back_populates="job_application")
    offer_letters = relationship("OfferLetter", back_populates="job_application")



    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_job_applications")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_job_applications")