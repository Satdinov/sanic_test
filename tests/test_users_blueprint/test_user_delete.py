import pytest
from sanic import Sanic

from database import User, UserLang, UserRole


@pytest.mark.asyncio
async def test_user_delete_admin(app: Sanic, admin: User):
    _, response = await app.asgi_client.post('/auth',
        json={
                'email': admin.email,
                'password': admin._raw_password,
        })
    assert response.status == 200

    _, response = await app.asgi_client.delete(f'/users/delete_user/{admin.id}')
    assert response.status == 200

@pytest.mark.asyncio
async def test_user_delete_user(app: Sanic, user: User):
    _, response = await app.asgi_client.post('/auth',
        json={
                'email': user.email,
                'password': user._raw_password,
        })
    assert response.status == 200

    _, response = await app.asgi_client.delete(f'/users/delete_user/{user.id}')
    assert response.status == 200
