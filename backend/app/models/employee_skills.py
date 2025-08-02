from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime
import enum

class SkillLevel(enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"

class EmployeeSkill(Base):
    __tablename__ = "employee_skills"
    
    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    
    proficiency_level = Column(Enum(SkillLevel), nullable=False, default=SkillLevel.beginner)
    years_of_experience = Column(Integer, default=0)
    is_certified = Column(Boolean, default=False)
    certification_name = Column(String(200), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    employee = relationship("Employee", back_populates="employee_skills", foreign_keys=[employee_id])
    skill = relationship("Skill", back_populates="employee_skills")
    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_employee_skills")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_employee_skills")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    __table_args__ = (
        {"extend_existing": True},
    )
