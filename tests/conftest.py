"""
@Time  ：2025-04-06
@Auth  ：Adam Lyu
"""

import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from httpx import AsyncClient, ASGITransport
from app.main import create_app
from app.core.config import settings
from app.models.membership import Membership
from app.models.user import User
from app.models.user_token import UserToken

# ✅ 测试用 MongoDB URI（推荐使用 test 数据库）
MONGO_TEST_URI = settings.MONGO_URI


# ✅ 避免 asyncio 事件循环冲突
@pytest.fixture(scope="function")
def anyio_backend():
    return "asyncio"


# ✅ 初始化 Beanie 模型（每个测试函数都跑一遍）
@pytest.fixture(scope="function", autouse=True)
async def init_db():
    client = AsyncIOMotorClient(MONGO_TEST_URI)
    db = client.get_default_database()

    await init_beanie(
        database=db,
        document_models=[
            User,
            UserToken,
            Membership,
        ]
    )


@pytest.fixture(scope="function")
async def test_app():
    app = create_app()
    return app


@pytest.fixture(scope="function")
async def test_client(test_app) -> AsyncClient:
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
