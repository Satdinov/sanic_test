import pytest
from sanic import Sanic

from database import User


@pytest.mark.asyncio
async def test_verify_user(app: Sanic, user: User):
    _, response = await app.asgi_client.post('/auth',
        json={
                'email': user.email,
                'password': user._raw_password,
        })
    assert response.status == 200

    _, response = await app.asgi_client.get('/auth/verify')
    assert response.status == 200

@pytest.mark.asyncio
async def test_verify_admin(app: Sanic, admin: User):
    _, response = await app.asgi_client.post('/auth',
        json={
                'email': admin.email,
                'password': admin._raw_password,
        })
    assert response.status == 200

    _, response = await app.asgi_client.get('/auth/verify')
    assert response.status == 200
