"""
@Time ： 2025-04-04
@Auth ： Adam Lyu
"""
from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_verified: bool
    role: str
