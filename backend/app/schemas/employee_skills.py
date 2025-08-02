from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

from app.schemas.skills import SkillOut

class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"


class EmployeeSkillBase(BaseModel):
    employee_id: Optional[int] = None
    skill_id: Optional[int] = None
    proficiency_level: Optional[SkillLevel] = SkillLevel.beginner
    years_of_experience: Optional[int] = 0
    is_certified: Optional[bool] = False
    certification_name: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None
    is_active: Optional[bool] = True

class EmployeeSkillCreate(EmployeeSkillBase):
    employee_id: int = Field(..., description="Employee ID is required")
    skill_id: int = Field(..., description="Skill ID is required")
    proficiency_level: SkillLevel = SkillLevel.beginner

class EmployeeSkillUpdate(EmployeeSkillBase):
    pass

class EmployeeSkillOut(EmployeeSkillBase):
    id: int
    created_by_user_id: int
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    # Optional nested objects for detailed responses
    skill: Optional[SkillOut] = None
    
    class Config:
        from_attributes = True

class PaginatedEmployeeSkills(BaseModel):
    count: int
    data: List[EmployeeSkillOut]

class EmployeeSkillListResponse(BaseModel):
    status: str
    result: PaginatedEmployeeSkills

# ========== COMBINED SCHEMAS FOR SPECIAL ENDPOINTS ==========

# class EmployeeWithSkills(BaseModel):
#     employee_id: int
#     employee_name: Optional[str] = None
#     skills: List[EmployeeSkillOut] = []
    
#     class Config:
#         from_attributes = True

class SkillWithEmployees(BaseModel):
    skill: SkillOut
    employees: List[EmployeeSkillOut] = []
    
    class Config:
        from_attributes = True


class SkillOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: Optional[str]
    is_active: Optional[bool]
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


from app.schemas.skills import SkillOut  # Assuming this schema exists

class SkillWithDetails(BaseModel):
    employee_id: int
    skill_id: int
    proficiency_level: str
    years_of_experience: int
    is_certified: bool
    certification_name: str
    notes: str
    is_active: bool
    id: int
    created_by_user_id: int
    updated_by_user_id: Optional[int]         # ✅ Fix
    created_at: datetime
    updated_at: Optional[datetime]            # ✅ Fix
    skill: SkillOut

    class Config:
        from_attributes = True


class EmployeeWithSkills(BaseModel):
    employee_id: int
    employee_name: str
    skills: List[SkillWithDetails]

    class Config:
        from_attributes = True
