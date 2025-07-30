from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime, date


# === Nested Schemas ===

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class EmployeeOut(BaseModel):
    id: int
    name: str  # Adjust according to your actual Employee model

    class Config:
        from_attributes = True


class RankOut(BaseModel):
    id: int
    title: str  # Adjust if your model uses a different field name

    class Config:
        from_attributes = True


# === Base Schema ===

class PromotionHistoryBase(BaseModel):
    employee_id: int
    previous_rank_id: Optional[int] = None
    new_rank_id: int
    promotion_date: date = Field(default_factory=lambda: datetime.utcnow().date())
    remarks: Optional[str] = None


# === Create Schema (used for POST) ===

class PromotionHistoryCreate(PromotionHistoryBase):
    pass


# === Update Schema (used for PUT/PATCH) ===

class PromotionHistoryUpdate(BaseModel):
    employee_id: Optional[int] = None
    previous_rank_id: Optional[int] = None
    new_rank_id: Optional[int] = None
    promotion_date: Optional[date] = None
    remarks: Optional[str] = None


# === Output Schema (used in GET responses) ===

class PromotionHistoryOut(PromotionHistoryBase):
    id: int
    created_by_user_id: Optional[int]
    updated_by_user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    # Optional nested outputs
    employee: Optional[EmployeeOut] = None
    previous_rank: Optional[RankOut] = None
    new_rank: Optional[RankOut] = None
    creator: Optional[UserOut] = None
    updater: Optional[UserOut] = None

    class Config:
        from_attributes = True


# === Paginated Response ===

class PaginatedPromotionHistory(BaseModel):
    count: int
    data: List[PromotionHistoryOut]


# === Top-level List Response ===

class PromotionHistoryListResponse(BaseModel):
    status: str
    result: PaginatedPromotionHistory
