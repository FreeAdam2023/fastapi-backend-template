"""
@Time ： 2025-04-05
@Auth ： Adam Lyu
"""

# app/core/init_indexes.py（可新建）
from pymongo import ASCENDING
from app.models.user import User

async def ensure_user_indexes():
    collection = User.get_motor_collection()
    await collection.create_index([("email", ASCENDING)], name="email_unique", unique=True)
    await collection.create_index([("username", ASCENDING)], name="username_unique", unique=True)
