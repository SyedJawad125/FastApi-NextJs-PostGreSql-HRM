# models/interview_schedule.py

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Text, Boolean, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

# === Interview Schedule Status Enum ===
class InterviewScheduleStatus(enum.Enum):
    scheduled = "scheduled"
    rescheduled = "rescheduled"
    canceled = "canceled"
    completed = "completed"

class InterviewSchedule(Base):
    __tablename__ = "interview_schedules"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    interview_id = Column(Integer, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False)
    scheduled_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    rescheduled_from_id = Column(Integer, ForeignKey("interview_schedules.id", ondelete="SET NULL"), nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    # Schedule Info
    scheduled_datetime = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=True)  # e.g. 30, 60
    time_zone = Column(String(50), default="Asia/Karachi")
    mode = Column(String(50), default="offline")  # online / offline / hybrid
    location = Column(String(255), nullable=True)

    # Status & Notes
    status = Column(SqlEnum(InterviewScheduleStatus), nullable=False, default=InterviewScheduleStatus.scheduled)
    remarks = Column(Text, nullable=True)

    # Audit Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # === Relationships ===
    interview = relationship("Interview", back_populates="interview_schedule")
    scheduler = relationship("User", foreign_keys=[scheduled_by_user_id], back_populates="scheduled_interviews")
    rescheduled_from = relationship("InterviewSchedule", remote_side=[id])  # self-referencing

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_schedules")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_schedules")
