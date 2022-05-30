from typing import Optional

from pydantic import BaseModel, validator
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

    @validator('email')
    def check_email(cls, value):  # noqa
        return value.lower()

    @validator('password')
    def check_password(cls, value):  # noqa
        if len(value) < 8:
            raise ValueError('short password')
        if not any(map(str.isdigit, value)):
            raise ValueError('password does not contain a digit')
        return value
