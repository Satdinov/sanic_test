import pytest
from sanic import Sanic

from database import User, UserLang, UserRole


@pytest.mark.asyncio
async def test_add_user_admin_en(app: Sanic):
    
    _, response = await app.asgi_client.post('/users/add_user', 
        json={
                'email': 'test@test.com',
                'password': 'password123Daswq2',
                'lang': UserLang.EN.value,
                'role': UserRole.Admin.value
    })

    assert response.status == 200

@pytest.mark.asyncio
async def test_add_user_user_en(app: Sanic):
    
    _, response = await app.asgi_client.post('/users/add_user', 
        json={
                'email': 'test@test.com',
                'password': 'password123Daswq2',
                'lang': UserLang.EN.value,
                'role': UserRole.User.value
    })

    assert response.status == 200

@pytest.mark.asyncio
async def test_add_user_admin_ru(app: Sanic):
    
    _, response = await app.asgi_client.post('/users/add_user', 
        json={
                'email': 'test@test.com',
                'password': 'password123Daswq2',
                'lang': UserLang.RU.value,
                'role': UserRole.Admin.value
    })

    assert response.status == 200

@pytest.mark.asyncio
async def test_add_user_user_ru(app: Sanic):
    
    _, response = await app.asgi_client.post('/users/add_user', 
        json={
                'email': 'test@test.com',
                'password': 'password123Daswq2',
                'lang': UserLang.RU.value,
                'role': UserRole.User.value
    })

    assert response.status == 200

@pytest.mark.asyncio
async def test_add_user_invalid_email(app: Sanic, invalid_emails):
    for invalid_email in invalid_emails:
        _, response = await app.asgi_client.post('/users/add_user', 
            json={
                    'email': invalid_email,
                    'password': 'password123Daswq2',
                    'role': UserRole.User.value,
                    'lang': UserLang.RU.value
        })
        assert response.status == 400

@pytest.mark.asyncio
async def test_add_user_invalid_password(app: Sanic, invalid_passwords):
    for invalid_password in invalid_passwords:
        _, response = await app.asgi_client.post('/users/add_user', 
            json={
                    'email': 'test@test.com',
                    'password': invalid_password,
                    'role': UserRole.User.value,
                    'lang': UserLang.EN.value
        })
        assert response.status == 400
