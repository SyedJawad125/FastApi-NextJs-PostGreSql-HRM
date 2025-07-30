from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum


class GrievanceStatus(enum.Enum):
    pending = "pending"
    under_review = "under_review"
    in_progress = "in_progress"
    resolved = "resolved"
    rejected = "rejected"
    closed = "closed"


class Grievance(Base):
    __tablename__ = "grievances"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    dept_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)

    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(GrievanceStatus), default=GrievanceStatus.pending, nullable=False)

    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # === Relationships ===
    employee = relationship("Employee", back_populates="grievances")
    department = relationship("Department", back_populates="grievances")

    creator = relationship("User", foreign_keys=[created_by], back_populates="created_grievances")
    updater = relationship("User", foreign_keys=[updated_by], back_populates="updated_grievances")
