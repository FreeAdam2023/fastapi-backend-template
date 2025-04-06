"""
@Time ： 2025-04-05
@Auth ： Adam Lyu
"""
# app/models/membership.py

from beanie import Document
from pymongo import ASCENDING
from pydantic import Field, ConfigDict
from datetime import datetime
from typing import Optional
from bson import ObjectId
from app.utils.pyobjectid import PyObjectId  # 👈 引入自定义 ObjectId 类型


class Membership(Document):
    user_id: PyObjectId  # 使用兼容 Pydantic 的 ObjectId 类型
    level: str  # free, basic, premium
    billing_cycle: str  # "monthly" or "yearly"
    started_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    is_active: bool = True
    auto_renew: bool = True
    payment_platform: Optional[str] = None
    transaction_id: Optional[str] = None

    # Pydantic v2 配置，允许任意类型，并在 JSON 中正确序列化 ObjectId
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    class Settings:
        name = "memberships"
        indexes = [
            [("user_id", ASCENDING)]
        ]
