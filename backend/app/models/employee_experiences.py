from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class EmployeeExperience(Base):
    __tablename__ = "employee_experiences"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)

    job_title = Column(String(100), nullable=False)
    company_name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    description = Column(Text)

    # Audit fields
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # --- Relationships ---
    # Link to Employee
    employee = relationship("Employee", back_populates="experiences")

    # Link to Users for audit trail
    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_experiences")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_experiences")
