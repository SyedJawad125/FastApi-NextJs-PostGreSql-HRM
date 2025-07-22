# from pydantic import BaseModel, EmailStr, ConfigDict, Field
# from typing import Optional, List
# from datetime import date
# from enum import Enum


# # ---------------------- Enums ----------------------

# class Gender(str, Enum):
#     MALE = "male"
#     FEMALE = "female"
#     OTHER = "other"

# class MaritalStatus(str, Enum):
#     SINGLE = "single"
#     MARRIED = "married"
#     DIVORCED = "divorced"
#     WIDOWED = "widowed"


# # ---------------------- Base Schema ----------------------

# class EmployeeProfileBase(BaseModel):
#     # --- Personal Information ---
#     employee_id: int = Field(..., description="Associated employee ID")
#     date_of_birth: date
#     gender: Gender
#     marital_status: MaritalStatus
#     nationality: str
#     national_id: str
#     passport_number: Optional[str] = None
#     passport_expiry: Optional[date] = None

#     # --- Contact Information ---
#     personal_email: Optional[EmailStr] = None
#     emergency_contact_name: str
#     emergency_contact_relationship: str
#     emergency_contact_phone: str
#     current_address: str
#     permanent_address: Optional[str] = None

#     # --- Education & Professional ---
#     highest_education: str
#     field_of_study: Optional[str] = None
#     institution: Optional[str] = None
#     graduation_year: Optional[int] = None
#     professional_certifications: Optional[List[str]] = None
#     skills: Optional[List[str]] = None

#     # --- Banking Information ---
#     bank_name: str
#     bank_account_number: str
#     bank_branch: Optional[str] = None
#     swift_code: Optional[str] = None

#     # --- Additional Information ---
#     blood_group: Optional[str] = None
#     medical_conditions: Optional[str] = None
#     dietary_restrictions: Optional[str] = None
#     languages: Optional[List[str]] = None
#     hobbies: Optional[List[str]] = None

#     # --- System Fields ---
#     created_by_user_id: Optional[int] = None
#     updated_by_user_id: Optional[int] = None

#     model_config = ConfigDict(from_attributes=True)


# # ---------------------- Create Schema ----------------------

# class EmployeeProfileCreate(EmployeeProfileBase):
#     """Schema for creating an employee profile."""
#     pass


# # ---------------------- Update Schema ----------------------

# class EmployeeProfileUpdate(BaseModel):
#     # --- Optional fields for partial update ---
#     date_of_birth: Optional[date] = None
#     gender: Optional[Gender] = None
#     marital_status: Optional[MaritalStatus] = None
#     nationality: Optional[str] = None
#     national_id: Optional[str] = None
#     passport_number: Optional[str] = None
#     passport_expiry: Optional[date] = None

#     personal_email: Optional[EmailStr] = None
#     emergency_contact_name: Optional[str] = None
#     emergency_contact_relationship: Optional[str] = None
#     emergency_contact_phone: Optional[str] = None
#     current_address: Optional[str] = None
#     permanent_address: Optional[str] = None

#     highest_education: Optional[str] = None
#     field_of_study: Optional[str] = None
#     institution: Optional[str] = None
#     graduation_year: Optional[int] = None
#     professional_certifications: Optional[List[str]] = None
#     skills: Optional[List[str]] = None

#     bank_name: Optional[str] = None
#     bank_account_number: Optional[str] = None
#     bank_branch: Optional[str] = None
#     swift_code: Optional[str] = None

#     blood_group: Optional[str] = None
#     medical_conditions: Optional[str] = None
#     dietary_restrictions: Optional[str] = None
#     languages: Optional[List[str]] = None
#     hobbies: Optional[List[str]] = None

#     updated_by_user_id: Optional[int] = None

#     model_config = ConfigDict(from_attributes=True)


# # ---------------------- Output Schema ----------------------

# class EmployeeProfileOut(EmployeeProfileBase):
#     id: int
#     created_at: date
#     updated_at: Optional[date] = None

#     model_config = ConfigDict(from_attributes=True)


# # ---------------------- Paginated Response ----------------------

# class PaginatedEmployeeProfiles(BaseModel):
#     count: int
#     data: List[EmployeeProfileOut]


# class EmployeeProfileListResponse(BaseModel):
#     status: str
#     result: PaginatedEmployeeProfiles

#     model_config = ConfigDict(from_attributes=True)




from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional, List
from datetime import date
from datetime import datetime
from enum import Enum
from .employee import Employee

# ---------------------- Enums ----------------------

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class MaritalStatus(str, Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"

# ---------------------- Base Schema ----------------------

class EmployeeProfileBase(BaseModel):
    # --- Personal Information ---
    employee_id: int = Field(..., description="Associated employee ID")
    date_of_birth: date
    gender: Gender
    marital_status: MaritalStatus
    nationality: str
    national_id: str
    passport_number: Optional[str] = None
    passport_expiry: Optional[date] = None

    # --- Contact Information ---
    personal_email: Optional[EmailStr] = None
    emergency_contact_name: str
    emergency_contact_relationship: str
    emergency_contact_phone: str
    current_address: str
    permanent_address: Optional[str] = None

    # --- Education & Professional ---
    highest_education: str
    field_of_study: Optional[str] = None
    institution: Optional[str] = None
    graduation_year: Optional[int] = None
    professional_certifications: Optional[List[str]] = Field(default_factory=list)
    skills: Optional[List[str]] = Field(default_factory=list)

    # --- Banking Information ---
    bank_name: str
    bank_account_number: str
    bank_branch: Optional[str] = None
    swift_code: Optional[str] = None

    # --- Additional Information ---
    blood_group: Optional[str] = None
    medical_conditions: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    languages: Optional[List[str]] = Field(default_factory=list)
    hobbies: Optional[List[str]] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

# ---------------------- Create Schema ----------------------

class EmployeeProfileCreate(EmployeeProfileBase):
    """Schema for creating an employee profile."""
    pass

# ---------------------- Update Schema ----------------------

class EmployeeProfileUpdate(BaseModel):
    # --- Optional fields for partial update ---
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    marital_status: Optional[MaritalStatus] = None
    nationality: Optional[str] = None
    national_id: Optional[str] = None
    passport_number: Optional[str] = None
    passport_expiry: Optional[date] = None

    personal_email: Optional[EmailStr] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    current_address: Optional[str] = None
    permanent_address: Optional[str] = None

    highest_education: Optional[str] = None
    field_of_study: Optional[str] = None
    institution: Optional[str] = None
    graduation_year: Optional[int] = None
    professional_certifications: Optional[List[str]] = None
    skills: Optional[List[str]] = None

    bank_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_branch: Optional[str] = None
    swift_code: Optional[str] = None

    blood_group: Optional[str] = None
    medical_conditions: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    languages: Optional[List[str]] = None
    hobbies: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)

# ---------------------- Output Schema ----------------------

class EmployeeProfileOut(EmployeeProfileBase):
    id: int
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
     # ✅ Include full employee object
    employee : Optional[Employee] = None
    model_config = ConfigDict(from_attributes=True)
    
# ---------------------- Paginated Response Schema ----------------------

class PaginatedEmployeeProfiles(BaseModel):
    count: int
    data: List[EmployeeProfileOut]

class EmployeeProfileListResponse(BaseModel):
    status: str
    result: PaginatedEmployeeProfiles

    model_config = ConfigDict(from_attributes=True)
