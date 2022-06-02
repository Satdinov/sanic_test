import pytest
from sanic import Sanic
import asyncio
from database import User, UserRole


async def test_add_user(app: Sanic):
    _, response = await app.asgi_client.post('/users/add_user',
        json={
            'email': 'test@test.ru',
            'password': 'Password1332',
            'lang': 'RU',
            'role': UserRole.User.value,
    })
    assert response.status == 200
