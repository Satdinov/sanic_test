import os
from importlib.metadata import files

import pytest
from sanic import Sanic

from database import Image, User, UserLang, UserRole


@pytest.mark.asyncio
async def test_add_image_admin(app: Sanic, admin:User, user:User):

    _, response = await app.asgi_client.post('/auth',
        json={
                'email': admin.email,
                'password': admin._raw_password,
        })
    assert response.status == 200

    upload_payload = {'image':  open(os.path.join('template', 'photo.jpg'), 'rb')}
    _, response = await app.asgi_client.post(f'/images/add_image/{admin.id}', files = upload_payload)
    assert response.status == 200

@pytest.mark.asyncio
async def test_add_image_user(app: Sanic, admin:User, user:User):

    _, response = await app.asgi_client.post('/auth',
        json={
                'email': user.email,
                'password': user._raw_password,
        })
    assert response.status == 200

    upload_payload = {'image':  open(os.path.join('template', 'photo.jpg'), 'rb')}
    _, response = await app.asgi_client.post(f'/images/add_image/{user.id}', files = upload_payload)
    assert response.status == 200
