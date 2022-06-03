import pytest
from sanic import Sanic

from database import User, UserLang, UserRole


@pytest.mark.asyncio
async def test_change_email_admin(app: Sanic, admin: User):
    _, response = await app.asgi_client.post('/auth',
        json={
                'email': admin.email,
                'password': admin._raw_password,
        })
    assert response.status == 200
    _, response = await app.asgi_client.patch(f'/users/change_email/{admin.id}', 
        json={
                'email': 'new@test.com',
        })
    assert response.status == 200

@pytest.mark.asyncio
async def test_change_email_user(app: Sanic, user: User):
    _, response = await app.asgi_client.post('/auth',
        json={
                'email': user.email,
                'password': user._raw_password,
        })
    assert response.status == 200
    _, response = await app.asgi_client.patch(f'/users/change_email/{user.id}', 
        json={
                'email': 'new@test.com',
        })
    assert response.status == 200

@pytest.mark.asyncio
async def test_invalid_change_email_admin(app: Sanic, invalid_emails, admin: User):
    _, response = await app.asgi_client.post('/auth',
    json={
            'email': admin.email,
            'password': admin._raw_password,
    })
    assert response.status == 200
    for invalid_email in invalid_emails:
        _, response = await app.asgi_client.patch(f'/users/change_email/{admin.id}', 
            json={
                    'email': invalid_email,
        })
        assert response.status == 400
