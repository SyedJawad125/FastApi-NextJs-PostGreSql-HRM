from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


# ===== ENUM DEFINITIONS =====

class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class SkillCategory(str, Enum):
    TECHNICAL = "technical"
    SOFT_SKILL = "soft_skill"
    LANGUAGE = "language"
    CERTIFICATION = "certification"
    TOOL = "tool"
    FRAMEWORK = "framework"


# ===== BASE SCHEMA =====

class SkillBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    category: Optional[SkillCategory] = SkillCategory.TECHNICAL
    is_active: Optional[bool] = True


# ===== CREATE/UPDATE SCHEMAS =====

class SkillCreate(SkillBase):
    name: str = Field(..., max_length=100)
    category: SkillCategory = SkillCategory.TECHNICAL  # enforce explicit choice

class SkillUpdate(SkillBase):
    pass


# ===== RESPONSE SCHEMA =====

class SkillOut(SkillBase):
    id: int
    created_by_user_id: int
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ===== PAGINATION & LIST RESPONSE =====

class PaginatedSkills(BaseModel):
    count: int
    data: List[SkillOut]

class SkillListResponse(BaseModel):
    status: str
    result: PaginatedSkills


# ===== RELATIONSHIP WITH EMPLOYEES =====

class EmployeeShort(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class SkillWithEmployees(SkillOut):
    employee_skills: List[EmployeeShort]

    class Config:
        from_attributes = True
