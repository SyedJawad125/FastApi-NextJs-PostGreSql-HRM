# from pydantic import BaseModel, Field
# from typing import Optional
# from datetime import date, datetime


# # ✅ Base schema used for shared fields
# class EmployeeContractBase(BaseModel):
#     employee_id: int
#     department_id: Optional[int] = None
#     contract_type: str = Field(..., max_length=100)
#     start_date: date
#     end_date: Optional[date] = None
#     salary: float
#     description: str


# # ✅ Schema for creating a new employee contract (no audit fields)
# class EmployeeContractCreate(EmployeeContractBase):
#     pass


# # ✅ Schema for updating an employee contract (no audit fields)
# class EmployeeContractUpdate(EmployeeContractBase):
#     pass


# # ✅ Schema for reading contract (include audit fields)
# class EmployeeContractOut(EmployeeContractBase):
#     id: int
#     created_by_user_id: int
#     updated_by_user_id: Optional[int] = None
#     created_at: Optional[datetime]
#     updated_at: Optional[datetime]

#     class Config:
#         from_attributes = True  # ✅ Allows ORM -> schema conversion


# # ✅ Paginated output schema (optional)
# class PaginatedEmployeeContracts(BaseModel):
#     count: int
#     data: list[EmployeeContractOut]


# # ✅ General API response wrapper (optional)
# class EmployeeContractListResponse(BaseModel):
#     status: str
#     result: PaginatedEmployeeContracts



# from pydantic import BaseModel, Field
# from typing import Optional, List
# from datetime import date, datetime


# # ✅ Base schema used for shared fields
# class EmployeeContractBase(BaseModel):
#     employee_id: int
#     department_id: Optional[int] = None
#     contract_type: str = Field(..., max_length=100)
#     start_date: date
#     end_date: Optional[date] = None
#     salary: float
#     description: str


# # ✅ Schema for creating a new employee contract (no audit fields)
# class EmployeeContractCreate(EmployeeContractBase):
#     pass


# # ✅ Schema for updating an employee contract (partial update allowed)
# class EmployeeContractUpdate(BaseModel):
#     employee_id: Optional[int] = None
#     department_id: Optional[int] = None
#     contract_type: Optional[str] = Field(None, max_length=100)
#     start_date: Optional[date] = None
#     end_date: Optional[date] = None
#     salary: Optional[float] = None
#     description: Optional[str] = None


# # ✅ Schema for reading contract (include audit fields)
# class EmployeeContractOut(EmployeeContractBase):
#     id: int
#     created_by_user_id: int
#     updated_by_user_id: Optional[int] = None
#     created_at: Optional[datetime]
#     updated_at: Optional[datetime]

#     class Config:
#         orm_mode = True  # Correct Pydantic config for SQLAlchemy model mapping


# # ✅ Paginated output schema
# class PaginatedEmployeeContracts(BaseModel):
#     count: int
#     data: List[EmployeeContractOut]


# # ✅ General API response wrapper
# class EmployeeContractListResponse(BaseModel):
#     status: str
#     result: PaginatedEmployeeContracts



from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


# ✅ Base schema used for shared fields
class EmployeeContractBase(BaseModel):
    employee_id: int
    department_id: Optional[int] = None
    contract_type: str = Field(..., max_length=100)
    start_date: date
    end_date: Optional[date] = None
    salary: float
    description: str

    class Config:
        from_attributes = True


# ✅ Schema for creating a new employee contract (no audit fields)
class EmployeeContractCreate(EmployeeContractBase):
    pass


# ✅ Schema for updating an employee contract (partial update allowed)
class EmployeeContractUpdate(BaseModel):
    employee_id: Optional[int] = None
    department_id: Optional[int] = None
    contract_type: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    salary: Optional[float] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# ✅ Schema for reading contract (include audit fields)
class EmployeeContractOut(EmployeeContractBase):
    id: int
    created_by_user_id: int
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ✅ Paginated output schema
class PaginatedEmployeeContracts(BaseModel):
    count: int
    data: List[EmployeeContractOut]

    class Config:
        from_attributes = True


# ✅ General API response wrapper
class EmployeeContractListResponse(BaseModel):
    status: str
    result: PaginatedEmployeeContracts

    class Config:
        from_attributes = True
