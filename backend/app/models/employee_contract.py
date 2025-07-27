from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class EmployeeContract(Base):
    __tablename__ = "employee_contracts"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    contract_type = Column(String(100), nullable=False)  # Not nullable
    start_date = Column(Date, nullable=False)            # Not nullable
    end_date = Column(Date, nullable=True)               # Still nullable
    salary = Column(Float, nullable=False)               # Not nullable
    description = Column(Text, nullable=False)           # Not nullable

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # ✅ Relationships
    employee = relationship("Employee", back_populates="contracts")
    department = relationship("Department", back_populates="employee_contracts")

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_employee_contracts")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_employee_contracts")
