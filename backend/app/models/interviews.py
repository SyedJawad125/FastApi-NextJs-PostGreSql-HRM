from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, String, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class InterviewMode(enum.Enum):
    online = "online"
    offline = "offline"
    phone = "phone"

class InterviewStatus(enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    job_application_id = Column(Integer, ForeignKey("job_applications.id"), nullable=False)
    interviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    interview_datetime = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=True)
    mode = Column(SqlEnum(InterviewMode), default=InterviewMode.online)
    status = Column(SqlEnum(InterviewStatus), default=InterviewStatus.scheduled)

    duration_minutes = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)

    # Additional
    interview_round = Column(Integer, default=1)
    interview_type = Column(String(50), nullable=True)  # e.g. Technical, HR
    panel_members = Column(Text, nullable=True)  # Could store as comma-separated or JSON
    result = Column(String(100), nullable=True)  # e.g., pass/fail/pending

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Tracking
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

    # === Relationships ===
    job_application = relationship("JobApplication", back_populates="interviews")
    interviewer = relationship("User", foreign_keys=[interviewer_id])
    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_interviews")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_interviews")
