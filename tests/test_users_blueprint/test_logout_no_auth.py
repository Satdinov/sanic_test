import pytest
from sanic import Sanic
import asyncio
from database import User, UserRole

@pytest.mark.asyncio
async def test_logout_no_auth(app: Sanic):
    _, response = await app.asgi_client.post('/auth/logout')
    assert response.status == 200

    _, response = await app.asgi_client.get('/auth/me')
    assert response.status == 401
