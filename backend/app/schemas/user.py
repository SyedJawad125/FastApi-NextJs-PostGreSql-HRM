from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr

# class UserCreate(UserBase):
#     password: str
#     role_id: int

class UserCreate(BaseModel):
    username: Optional[str] = None
    email: EmailStr
    password: str
    # role_id: int
    is_superuser: Optional[bool] = False  # default to False
    role_id: Optional[int] = None         # Optional, validated in endpoint logic
    employee_id: int  # ✅ Must link to an existing employee


# class UserLogin(BaseModel):  # This was missing
#     email: EmailStr
#     password: 


class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserOut(UserBase):
    id: int
    username: Optional[str] = None
    is_active: bool
    employee_id: int  # ✅ included in response
    
    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None
    token_type: str | None = None