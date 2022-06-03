import pytest
from sanic import Sanic

from database import User, UserRole, UserLang


@pytest.mark.asyncio
async def test_change_email_admin(app: Sanic, admin: User):
   # breakpoint()
    _, response = await app.asgi_client.post('/auth',
        json={
                'email': admin.email,
                'password': admin._raw_password,
        })
    assert response.status == 200
    
    _, response = await app.asgi_client.post(f'/users/change_email/{admin.id}', 
        json={
                'email': 'new@test.com',
    })
    assert response.status == 200

'''
@pytest.mark.asyncio
async def test_invalid_change_email_admin(app: Sanic, invalid_emails, user: User):
    _, response = await app.asgi_client.post(f'/users/change_email/{user.id}', 
        json={
                'email': invalid_emails,
                #'role': UserRole.Admin.value
    })
    assert response.status == 400
'''
