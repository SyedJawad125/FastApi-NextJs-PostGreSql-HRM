from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime
import enum

# Optional: Status Enum for the request
class OvertimeStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class OvertimeRequest(Base):
    __tablename__ = "overtime_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    request_user_id = Column(Integer, ForeignKey("users.id"))  # person who submitted request

    reason = Column(Text, nullable=False)
    hours_requested = Column(Integer, nullable=False)
    date_requested = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(OvertimeStatus), default=OvertimeStatus.PENDING)

    # Relationships
    employee = relationship("Employee", back_populates="overtime_requests")
    department = relationship("Department", back_populates="overtime_requests")
    request_user = relationship("User", back_populates="submitted_overtime_requests", foreign_keys=[request_user_id])
    approved_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_by = relationship("User", back_populates="approved_overtime_requests", foreign_keys=[approved_by_user_id])

    # Audit fields
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    creator = relationship("User", back_populates="created_overtime_requests", foreign_keys=[created_by_user_id])
    updater = relationship("User", back_populates="updated_overtime_requests", foreign_keys=[updated_by_user_id])

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
