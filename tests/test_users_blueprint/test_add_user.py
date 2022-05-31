import pytest
from sanic import Sanic

from database import User, UserRole

@pytest.mark.asyncio
async def test_add_user_admin(app: Sanic):
    _, response = await app.asgi_client.post('/api/users/add_user', json={
                                                                        'email': 'test',
                                                                        'password': await app.ctx.password_hasher.async_hash('password'),
                                                                        'role': UserRole.USER.value })
    assert response.status == 200
