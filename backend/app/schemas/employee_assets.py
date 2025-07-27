from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date, datetime


# Base schema shared by Create and Out
class EmployeeAssetBase(BaseModel):
    asset_name: str = Field(..., max_length=100)
    asset_type: str = Field(..., max_length=50)
    brand: Optional[str] = Field(None, max_length=50)
    model: Optional[str] = Field(None, max_length=100)
    serial_number: Optional[str] = Field(None, max_length=100)

    employee_id: Optional[int] = None
    department_id: Optional[int] = None

    issued_date: Optional[date] = None
    return_date: Optional[date] = None
    condition_issued: Optional[str] = Field(None, max_length=100)
    condition_returned: Optional[str] = Field(None, max_length=100)
    remarks: Optional[str] = None


# Schema for creating an asset (created_by handled internally)
class EmployeeAssetCreate(EmployeeAssetBase):
    pass


# Schema for updating an asset (partial fields)
class EmployeeAssetUpdate(BaseModel):
    asset_name: Optional[str] = Field(None, max_length=100)
    asset_type: Optional[str] = Field(None, max_length=50)
    brand: Optional[str] = Field(None, max_length=50)
    model: Optional[str] = Field(None, max_length=100)
    serial_number: Optional[str] = Field(None, max_length=100)

    employee_id: Optional[int] = None
    department_id: Optional[int] = None

    issued_date: Optional[date] = None
    return_date: Optional[date] = None
    condition_issued: Optional[str] = Field(None, max_length=100)
    condition_returned: Optional[str] = Field(None, max_length=100)
    remarks: Optional[str] = None


# Schema for outputting data (includes audit fields)
class EmployeeAssetOut(EmployeeAssetBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# List output for pagination
class PaginatedEmployeeAssets(BaseModel):
    count: int
    data: List[EmployeeAssetOut]


# Final response wrapper
class EmployeeAssetListResponse(BaseModel):
    status: str
    result: PaginatedEmployeeAssets
