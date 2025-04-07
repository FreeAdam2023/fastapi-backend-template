"""
@Time ： 2025-04-06
@Auth ： Adam Lyu
"""

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_user_profile(test_client: AsyncClient):
    response = await test_client.get("/api/v1/user/me")
    assert response.status_code in [200, 401]
