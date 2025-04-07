"""
@Time ： 2025-04-06
@Auth ： Adam Lyu
"""

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_invalid_credentials(test_client: AsyncClient):
    payload = {"email": "wrong@example.com", "password": "wrongpass"}
    response = await test_client.post("api/v1/auth/login", json=payload)
    assert response.status_code == 401
