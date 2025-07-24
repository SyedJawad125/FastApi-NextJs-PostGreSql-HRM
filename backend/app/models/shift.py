from sqlalchemy import Column, Integer, String, Time, DateTime
from datetime import datetime
from app.database import Base
from sqlalchemy.orm import relationship

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)  # e.g. "Morning Shift"
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    break_minutes = Column(Integer, default=0)
    grace_period_minutes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Optional: Back relationship
    employees = relationship("Employee", back_populates="shift")
    attendances = relationship("Attendance", back_populates="shift")
    timesheets = relationship("Timesheet", back_populates="shift")
    
    shift_assignments = relationship("ShiftAssignment", back_populates="shift", cascade="all, delete-orphan")
