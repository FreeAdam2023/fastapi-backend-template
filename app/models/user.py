"""
@Time  ：2025-04-04
@Auth  ：Adam Lyu
"""
# app/models/user.py

from beanie import Document
from pydantic import EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional
from bson import ObjectId
from pymongo import ASCENDING  # ✅ 用于正确创建索引


class User(Document):
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_verified: bool = False
    role: str = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    class Settings:
        name = "users"
        indexes = [
            [("email", ASCENDING)],     # ✅ 正确的索引写法
            [("username", ASCENDING)]   # ✅ 正确的索引写法
        ]
