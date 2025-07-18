from typing import Optional, List
from pydantic import BaseModel


# ✅ Shared base schema
class ImageCategoryBase(BaseModel):
    category: str


# ✅ For image category creation
class ImageCategoryCreate(ImageCategoryBase):
    created_by_user_id: Optional[int] = None

    class Config:
        extra = "forbid"


# ✅ For image category update
class ImageCategoryUpdate(BaseModel):
    category: Optional[str] = None
    updated_by_user_id: Optional[int] = None

    class Config:
        extra = "forbid"


# ✅ Minimal nested image output schema
class ImageOut(BaseModel):
    id: int
    image_url: str

    class Config:
        from_attributes = True


# ✅ Full image category response schema
class ImageCategory(ImageCategoryBase):
    id: int
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    images: List[ImageOut] = []

    class Config:
        from_attributes = True


# ✅ Paginated list wrapper
class PaginatedImageCategory(BaseModel):
    count: int
    data: List[ImageCategory]


# ✅ API response wrapper
class ImageCategoryListResponse(BaseModel):
    status: str
    result: PaginatedImageCategory
