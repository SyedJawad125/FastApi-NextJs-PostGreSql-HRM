from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class EmployeeLoan(Base):
    __tablename__ = "employee_loans"

    id = Column(Integer, primary_key=True, index=True)
    
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    # Who approved the loan
    approved_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Audit fields
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    amount = Column(Float, nullable=False)
    loan_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    issue_date = Column(Date, nullable=False, default=datetime.utcnow)
    due_date = Column(Date, nullable=True)
    status = Column(String(50), nullable=False, default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", back_populates="loans")
    department = relationship("Department", back_populates="loans")

    approved_by = relationship("User", foreign_keys=[approved_by_user_id], back_populates="approved_loans")
    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_loans")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_loans")
