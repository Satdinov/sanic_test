from typing import Optional

from pydantic import BaseModel
from sanic_ext import openapi

from database import UserLang, UserRole


class AddUserSchema:
    email = openapi.String(description='User email')
    password = openapi.String(description='User password')
    lang = openapi.String(description='User lang', oneOf=('EN', 'RU'))
    role = openapi.String(description='User role', oneOf=('Admin', 'User'))


class ChangeEmailSchema:
    email = openapi.String(description='New user email')


class AddUserModel(BaseModel):
    email: str
    password: str
    lang: Optional[UserLang]
    role: Optional[UserRole]
