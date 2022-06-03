import pytest
from sanic import Sanic

from database import User, UserLang, UserRole


@pytest.mark.asyncio
async def test_get_user_user(app: Sanic, admin: User):
    _, response = await app.asgi_client.post('/auth',
        json={
                'email': admin.email,
                'password': admin._raw_password,
        })
    assert response.status == 200

    _, response = await app.asgi_client.get(f'/users/get_user/{admin.id}')
    assert response.status == 200

@pytest.mark.asyncio
async def test_get_user_admin(app: Sanic, admin: User):
    _, response = await app.asgi_client.post('/auth',
        json={
                'email': admin.email,
                'password': admin._raw_password,
        })
    assert response.status == 200

    _, response = await app.asgi_client.get(f'/users/get_user/{admin.id}')
    assert response.status == 200
