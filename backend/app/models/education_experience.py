from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class EducationExperience(Base):
    __tablename__ = "education_experiences"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to the Employee table
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)

    institution_name = Column(String(255), nullable=False)   # School/College/University
    degree = Column(String(100), nullable=False)              # Matric, FSc, BSc, etc.
    field_of_study = Column(String(100), nullable=True)       # Computer Science, etc.
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    grade = Column(String(50), nullable=True)                 # A+, 3.8 GPA, etc.
    description = Column(Text, nullable=True)

    # Audit fields
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # --- Relationships ---
    # Link to Employee
    employee = relationship("Employee", back_populates="educations")

    # Link to Users for audit trail
    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_educations")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_educations")
