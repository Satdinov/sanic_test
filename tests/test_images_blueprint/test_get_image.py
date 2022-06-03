import os
from importlib.metadata import files

import pytest
from sanic import Sanic

from database import Image, User, UserLang, UserRole


@pytest.mark.asyncio
async def test_get_image_admin(app: Sanic, admin:User, user_image:Image):

    _, response = await app.asgi_client.post('/auth',
        json={
                'email': admin.email,
                'password': admin._raw_password,
        })
    assert response.status == 200
    
    _, response = await app.asgi_client.get(f'/images/get_image/{admin.id}')
    assert response.status == 200

@pytest.mark.asyncio
async def test_get_image_user(app: Sanic, user:User,):

    _, response = await app.asgi_client.post('/auth',
        json={
                'email': user.email,
                'password': user._raw_password,
        })
    assert response.status == 200
    
    _, response = await app.asgi_client.get(f'/images/get_image/{user.id}')
    assert response.status == 200
