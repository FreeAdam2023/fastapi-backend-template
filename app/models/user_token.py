"""
@Time ： 2025-04-05
@Auth ： Adam Lyu
"""

# app/models/user_token.py

from beanie import Document
from pydantic import Field, ConfigDict
from datetime import datetime
from typing import Optional
from bson import ObjectId
from pymongo import ASCENDING
from app.utils.pyobjectid import PyObjectId  # ✅ 自定义 Pydantic 兼容 ObjectId 类型


class UserToken(Document):
    user_id: PyObjectId = Field(...)  # ✅ 显式指定类型为 ObjectId 兼容类型
    device_name: str                  # 设备名，例如 "iPhone 15", "Chrome on Mac"
    token: str                        # JWT token 本体
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    is_active: bool = True

    # ✅ Pydantic v2 配置方式
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}  # 输出时将 ObjectId 转为 str
    )

    class Settings:
        name = "user_tokens"  # ✅ MongoDB collection 名称
        indexes = [
            [("user_id", ASCENDING)]
        ]
