"""
@Time ： 2025-04-05
@Auth ： Adam Lyu
@Desc ：认证模块相关 schema
"""

from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from app.schemas.user import UserResponse


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=30)
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    # ✅ 用邮箱登录，注意没有 username 字段
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None  # ✅ 可选，仅在登录/刷新时返回
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse
