from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)

    employees = relationship("Employee", back_populates="department")
    ranks = relationship("Rank", back_populates="department")
    employee_salaries = relationship("EmployeeSalary", back_populates="department")
    salary_structures = relationship("SalaryStructure", back_populates="department")
    salary_histories = relationship("SalaryHistory", back_populates="department")
    payslips = relationship("Payslip", back_populates="department")

    holidays = relationship("HolidayCalendar", back_populates="department")
    recruitments = relationship("Recruitment", back_populates="department")
    trainings = relationship("Training", back_populates="department", cascade="all, delete-orphan")
    assets = relationship("EmployeeAsset", back_populates="department")
    employee_contracts = relationship("EmployeeContract", back_populates="department")

    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_departments")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_departments")


