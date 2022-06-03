import pytest
from sanic import Sanic

from database import User
from tests.conftest import invalid_emails, invalid_passwords


@pytest.mark.asyncio
async def test_auth_admin(app: Sanic, admin: User):
    _, response = await app.asgi_client.post('/auth',
        json={
                'email': admin.email,
                'password': admin._raw_password,
        })
    assert response.status == 200

@pytest.mark.asyncio
async def test_auth_user(app: Sanic, user: User):
    _, response = await app.asgi_client.post('/auth',
        json={
                'email': user.email,
                'password': user._raw_password,
        })
    assert response.status == 200


@pytest.mark.asyncio
async def test_auth_invalid_email_admin(app: Sanic, admin: User, invalid_emails):
    for invalid_email in invalid_emails:
        _, response = await app.asgi_client.post('/auth',
            json={
                    'email': invalid_email,
                    'password': admin._raw_password,
        })
        assert response.status == 400

@pytest.mark.asyncio
async def test_auth_invalid_password_admin(app: Sanic, admin: User, invalid_passwords):
    for invalid_password in invalid_passwords:
        _, response = await app.asgi_client.post('/auth',
            json={
                    'email': admin.email,
                    'password': invalid_password,
        })
        assert response.status == 401

@pytest.mark.asyncio
async def test_auth_invalid_email_user(app: Sanic, user: User, invalid_emails):
    for invalid_email in invalid_emails:
        _, response = await app.asgi_client.post('/auth',
            json={
                    'email': invalid_email,
                    'password': user._raw_password,
        })
        assert response.status == 400

@pytest.mark.asyncio
async def test_auth_invalid_password_user(app: Sanic, user: User, invalid_passwords):
    for invalid_password in invalid_passwords:
        _, response = await app.asgi_client.post('/auth',
            json={
                    'email': user.email,
                    'password': invalid_password,
        })
        assert response.status == 401
