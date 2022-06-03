import pytest
from sanic import Sanic

from database import User, UserRole, UserLang


@pytest.mark.asyncio
async def test_add_user_admin(app: Sanic):
    
    _, response = await app.asgi_client.post('/users/add_user', 
        json={
                'email': 'test@test.com',
                'password': 'password123Daswq2',
                'lang': UserLang.EN.value,
                'role': UserRole.Admin.value
    })

    assert response.status == 200

@pytest.mark.asyncio
async def test_add_user_invalid_login(app: Sanic, invalid_emails):
    _, response = await app.asgi_client.post('/users/add_user', 
        json={
                'email': invalid_emails,
                'password': 'password123Daswq2',
                'role': UserRole.User.value
    })
    assert response.status == 400

@pytest.mark.asyncio
async def test_add_user_invalid_password(app: Sanic, invalid_passwords):
    _, response = await app.asgi_client.post('/users/add_user', 
        json={
                'email': 'test@test.com',
                'password': invalid_passwords,
                'role': UserRole.User.value
    })
    assert response.status == 400