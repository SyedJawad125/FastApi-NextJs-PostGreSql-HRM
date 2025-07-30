from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class TravelExpenseStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    paid = "paid"
    cancelled = "cancelled"

class TravelExpense(Base):
    __tablename__ = "travel_expenses"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    submitted_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    # Fields
    purpose = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    travel_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    total_amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    status = Column(SqlEnum(TravelExpenseStatus), default=TravelExpenseStatus.pending)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", back_populates="travel_expenses")
    department = relationship("Department", back_populates="travel_expenses")
    submitter = relationship("User", foreign_keys=[submitted_by_user_id])
    approver = relationship("User", foreign_keys=[approved_by_user_id])

    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_travel_expenses")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_travel_expenses")


