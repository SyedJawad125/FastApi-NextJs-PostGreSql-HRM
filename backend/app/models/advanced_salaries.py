from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base
from datetime import datetime
import enum


class AdvanceStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"


class AdvancedSalary(Base):
    __tablename__ = "advanced_salaries"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    reason = Column(String, nullable=True)
    request_date = Column(Date, nullable=False, default=datetime.utcnow)
    approved_date = Column(Date, nullable=True)
    status = Column(Enum(AdvanceStatus), default=AdvanceStatus.PENDING)

    # Foreign Keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", back_populates="advanced_salaries")
    department = relationship("Department", back_populates="advanced_salaries")

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_advanced_salaries")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_advanced_salaries")
