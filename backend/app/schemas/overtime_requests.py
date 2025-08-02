# from pydantic import BaseModel
# from typing import Optional, List
# from datetime import datetime
# from enum import Enum

# # ✅ Nested output schemas (same as in your example)
# class UserOut(BaseModel):
#     id: int
#     username: str

#     class Config:
#         from_attributes = True


# class EmployeeOut(BaseModel):
#     id: int
#     name: str

#     class Config:
#         from_attributes = True


# class DepartmentOut(BaseModel):
#     id: int
#     name: str

#     class Config:
#         from_attributes = True


# # ✅ Enum for status
# class OvertimeStatus(str, Enum):
#     PENDING = "pending"
#     APPROVED = "approved"
#     REJECTED = "rejected"

# # ✅ Base schema (shared fields)
# class OvertimeRequestBase(BaseModel):
#     reason: str
#     hours_requested: int
#     status: Optional[OvertimeStatus] = OvertimeStatus.PENDING

# # ✅ Create schema (payload)
# class OvertimeRequestCreate(OvertimeRequestBase):
#     employee_id: int
#     department_id: int
#     request_user_id: int

# # ✅ Update/Patch schema (payload)
# class OvertimeRequestUpdate(BaseModel):
#     reason: Optional[str] = None
#     hours_requested: Optional[int] = None
#     status: Optional[OvertimeStatus] = None
#     employee_id: Optional[int] = None
#     department_id: Optional[int] = None
#     request_user_id: Optional[int] = None
#     approved_by_user_id: Optional[int] = None

# # ✅ Output schema (GET response)
# class OvertimeRequestOut(OvertimeRequestBase):
#     id: int
#     employee_id: int
#     department_id: int
#     request_user_id: int

#     approved_by_user_id: Optional[int] = None
#     created_by_user_id: Optional[int] = None
#     updated_by_user_id: Optional[int] = None

#     created_at: Optional[datetime]
#     updated_at: Optional[datetime]

#     # Relationships
#     employee: Optional[EmployeeOut] = None
#     department: Optional[DepartmentOut] = None
#     request_user: Optional[UserOut] = None
#     approved_by: Optional[UserOut] = None
#     creator: Optional[UserOut] = None
#     updater: Optional[UserOut] = None

#     class Config:
#         from_attributes = True

# # ✅ Paginated wrapper for list response
# class PaginatedOvertimeRequest(BaseModel):
#     count: int
#     data: List[OvertimeRequestOut]

# class OvertimeRequestListResponse(BaseModel):
#     status: str
#     result: PaginatedOvertimeRequest




from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ✅ Nested output schemas
class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    
    class Config:
        from_attributes = True

class EmployeeOut(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    user_id: Optional[int] = None  # ✅ This is what ensures it's returned

    class Config:
        from_attributes = True


class DepartmentOut(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

# ✅ Enum for status
class OvertimeStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# ✅ Base schema (shared fields)
class OvertimeRequestBase(BaseModel):
    reason: str = Field(..., min_length=10, max_length=1000, description="Reason for overtime request")
    hours_requested: int = Field(..., ge=1, le=24, description="Hours requested (1-24)")
    
    @field_validator('reason')
    @classmethod
    def validate_reason(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Reason cannot be empty')
        return v.strip()

# ✅ Create schema (payload)
class OvertimeRequestCreate(OvertimeRequestBase):
    department_id: int = Field(..., ge=1, description="Valid department ID")

    @field_validator('department_id')
    @classmethod
    def validate_department_id(cls, v):
        if v < 1:
            raise ValueError("Department ID must be a positive integer.")
        return v

# ✅ Update schema (payload)
class OvertimeRequestUpdate(BaseModel):
    reason: Optional[str] = Field(None, min_length=10, max_length=1000)
    hours_requested: Optional[int] = Field(None, ge=1, le=24)
    
    @field_validator('reason')
    @classmethod
    def validate_reason(cls, v):
        if v is not None and (not v or v.strip() == ""):
            raise ValueError('Reason cannot be empty')
        return v.strip() if v else v

# ✅ Admin update schema
class OvertimeRequestAdminUpdate(OvertimeRequestUpdate):
    status: Optional[OvertimeStatus] = None
    approved_by_user_id: Optional[int] = None

# ✅ Output schema
class OvertimeRequestOut(OvertimeRequestBase):
    id: int
    employee_id: int
    department_id: int
    request_user_id: int
    status: OvertimeStatus
    
    approved_by_user_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    
    date_requested: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    employee: Optional[EmployeeOut] = None
    department: Optional[DepartmentOut] = None
    request_user: Optional[UserOut] = None
    approved_by: Optional[UserOut] = None
    creator: Optional[UserOut] = None
    updater: Optional[UserOut] = None
    
    class Config:
        from_attributes = True

# ✅ Detailed output schema
class OvertimeRequestDetailOut(OvertimeRequestOut):
    can_edit: bool = Field(default=False, description="Whether current user can edit this request")
    can_approve: bool = Field(default=False, description="Whether current user can approve this request")
    is_owner: bool = Field(default=False, description="Whether current user owns this request")

# ✅ Paginated wrapper
class PaginatedOvertimeRequest(BaseModel):
    count: int
    data: List[OvertimeRequestOut]
    page: Optional[int] = None
    page_size: Optional[int] = None
    total_pages: Optional[int] = None

class OvertimeRequestListResponse(BaseModel):
    status: str = "SUCCESSFUL"
    result: PaginatedOvertimeRequest

# ✅ Response schemas
class OvertimeRequestCreateResponse(BaseModel):
    status: str = "SUCCESSFUL"
    message: str = "Overtime request created successfully"
    data: OvertimeRequestOut

class OvertimeRequestUpdateResponse(BaseModel):
    status: str = "SUCCESSFUL"
    message: str = "Overtime request updated successfully"
    data: OvertimeRequestOut

# ✅ Statistics schema
class OvertimeRequestStats(BaseModel):
    total_requests: int
    pending_requests: int
    approved_requests: int
    rejected_requests: int
    total_hours_requested: int
    total_hours_approved: int

