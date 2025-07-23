from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# ---------------- Many-to-Many Table for Employee-Holidays ----------------
employee_holidays = Table(
    "employee_holidays",
    Base.metadata,
    Column("holiday_id", Integer, ForeignKey("holiday_calendars.id")),
    Column("employee_id", Integer, ForeignKey("employees.id"))
)

# ---------------- HolidayCalendar Model ----------------
class HolidayCalendar(Base):
    __tablename__ = "holiday_calendars"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(Date, nullable=False)
    is_optional = Column(Boolean, default=False)
    is_national = Column(Boolean, default=True)

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(Date, server_default=func.current_date())
    updated_at = Column(Date, onupdate=func.current_date())

    # ---------------- Relationships ----------------
    department = relationship("Department", back_populates="holidays")
    created_by = relationship("User", foreign_keys=[created_by_user_id])
    updated_by = relationship("User", foreign_keys=[updated_by_user_id])

    # Many-to-many with Employees
    employees = relationship("Employee", secondary=employee_holidays, backref="holidays")
