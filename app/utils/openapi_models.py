from pydantic import BaseModel, EmailStr, validator
from sanic_ext import openapi


class ResponseSchema:
    description = openapi.String(description='Description')
    status = openapi.Integer(description='Status code')
    message = openapi.String(description='Message')


class AuthErrorSchema:
    reasons = openapi.Array(openapi.String(description='Reason'))
    exception = openapi.String(description='Exception')


class AuthSchema:
    email = openapi.Email(description='User email', required=True, nullable=False)
    password = openapi.Password(description='User password', required=True, nullable=False)


class AuthModel(BaseModel):
    email: EmailStr
    password: str

    @validator('email')
    def check_email(cls, value):  # noqa
        return value.lower()


class AuthTokensSchema:
    access_token = openapi.String(description='Access token')
    refresh_token = openapi.String(description='Refresh token')


class AccessTokenSchema:
    access_token = openapi.String(description='Access token')


class RefreshTokenSchema:
    refresh_token = openapi.String(description='Refresh token')


class AuthVerifySchema:
    valid = openapi.Boolean(description='Is valid authentication')


class UserSchema:
    id = openapi.String(description='User ID', format='uuid')
    create_datetime = openapi.DateTime(description='User ISO create datetime')
    update_datetime = openapi.DateTime(description='User ISO update datetime')
    role = openapi.String(description='User role', oneOf=('ADMIN', 'USER'), example='USER')
    email = openapi.Email(description='User email')
    firstname = openapi.String(description='User firstname')
    lastname = openapi.String(description='User lastname')


class CurrentUserSchema:
    me = UserSchema
