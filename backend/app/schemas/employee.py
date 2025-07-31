# from pydantic import BaseModel, EmailStr
# from datetime import date
# from typing import List, Optional

# class EmployeeBase(BaseModel):
#     first_name: str
#     last_name: str
#     email: EmailStr
#     phone_number: Optional[str] = None
#     hire_date: date
#     job_title: str
#     salary: float
#     department_id: int
#     rank_id: Optional[int] = None  # ✅ Allow rank_id to be nullable

# class EmployeeCreate(EmployeeBase):
#    class Config:
#         extra = "forbid"


# class Employee(EmployeeBase):
#     id: int
    
#     class Config:
#         from_attributes = True  # Previously called orm_mode in Pydantic v1

# class PaginatedEmployees(BaseModel):
#     count: int
#     data: List[Employee]

# # ✅ Add this for final API response
# class EmployeeListResponse(BaseModel):
#     status: str
#     result: PaginatedEmployees

# class EmployeeUpdate(BaseModel):
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None
#     email: Optional[EmailStr] = None
#     phone_number: Optional[str] = None
#     hire_date: Optional[date] = None
#     job_title: Optional[str] = None
#     salary: Optional[float] = None
#     department_id: Optional[int] = None
#     rank_id: Optional[int] = None

#     class Config:
#         extra = "forbid"



from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional

from app.schemas.user import UserOut

# ✅ Base for create/update, not used in response
class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    hire_date: date
    job_title: str
    salary: float
    department_id: int
    rank_id: Optional[int] = None  # ✅ Allow rank_id to be nullable


# ✅ Create schema (used in POST payload)
class EmployeeCreate(EmployeeBase):
    class Config:
        extra = "forbid"


# ✅ Update schema (used in PUT/PATCH payload)
class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    hire_date: Optional[date] = None
    job_title: Optional[str] = None
    salary: Optional[float] = None
    department_id: Optional[int] = None
    rank_id: Optional[int] = None

    class Config:
        extra = "forbid"

# ✅ Employee Response Schema (including optional user info)
# ✅ Response schema (used in GET)
class Employee(BaseModel):
    id: int
    name: str  # <-- full name: first_name + last_name
    email: EmailStr
    phone_number: Optional[str]
    hire_date: date
    job_title: str
    salary: float
    department_id: int
    rank_id: Optional[int]
    user: Optional[UserOut] = None  # 👈 show linked user info if exists

    class Config:
        from_attributes = True  # required to work with SQLAlchemy models


# ✅ Pagination and wrapper schema for API response
class PaginatedEmployees(BaseModel):
    count: int
    data: List[Employee]

class EmployeeListResponse(BaseModel):
    status: str
    result: PaginatedEmployees
