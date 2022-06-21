from datetime import datetime
from typing import Dict, List, Optional

from argon2.exceptions import VerificationError
from sanic import Sanic, json
from sanic.request import Request
from sanic_ext import openapi, validate
from sanic_jwt import Initialize, exceptions
from sanic_jwt.endpoints import (
    AuthenticateEndpoint, BaseEndpoint, RefreshEndpoint, RetrieveUserEndpoint, VerifyEndpoint
)
from sentry_sdk import configure_scope

from database import User

from .openapi_models import (
    AccessTokenSchema, AuthErrorSchema, AuthModel, AuthSchema, AuthTokensSchema, AuthVerifySchema, CurrentUserSchema,
    RefreshTokenSchema, ResponseSchema
)


@validate(json=AuthModel)
async def authenticate(request: Request, body: AuthModel):
    user = await loaders.users_query(email=str(body.email).lower()).first()
    if user:
        try:
            await request.app.ctx.password_hasher.async_verify(user.password, str(body.password))
        except VerificationError:
            pass
        else:
            if await request.app.ctx.password_hasher.async_check_needs_rehash(user.password):
                rehashed_password = await request.app.ctx.password_hasher.async_hash(body.password)
                await user.update(password=rehashed_password, update_datetime=datetime.utcnow()).apply()

            with configure_scope() as scope:
                scope.user = {
                    'id': str(user.id),
                    'email': user.email.lower(),
                    'role': user.role.value
                }

            return user
    raise exceptions.AuthenticationFailed('Incorrect email or password')


async def retrieve_user(request: Request, payload: Dict) -> Optional[User]:  # pylint: disable=unused-argument
    user = await loaders.users_query(user_id=payload['id']).first()
    if not user:
        raise exceptions.InvalidAuthorizationHeader()

    with configure_scope() as scope:
        scope.user = {
            'id': str(user.id),
            'email': user.email.lower(),
            'role': user.role.value
        }

    return user


def user_refresh_token_key(user_id: str) -> str:
    return f'refresh_token_{user_id}'


async def store_refresh_token(request: Request, user_id: str, refresh_token: str):
    await request.app.ctx.redis.set(user_refresh_token_key(user_id), refresh_token)


async def retrieve_refresh_token(request: Request, user_id: str):
    return await request.app.ctx.redis.get(user_refresh_token_key(user_id))


async def scope_extender(user: User) -> List[str]:
    return [user.role.value]


class LogoutEndpoint(BaseEndpoint):
    async def post(self, request: Request, *args, **kwargs):  # pylint: disable=unused-argument
        user_id = request.app.ctx.auth.extract_user_id(request)
        await request.app.ctx.redis.delete(user_refresh_token_key(user_id))

        response = json({'status': 200, 'message': 'OK', 'description': None})
        if 'access_token' in request.cookies:
            del response.cookies['access_token']
        if 'refresh_token' in request.cookies:
            del response.cookies['refresh_token']

        return response


def register_openapi_routes():
    openapi.operation('authenticate')(AuthenticateEndpoint.post)
    openapi.summary('Authenticate')(AuthenticateEndpoint.post)
    AuthenticateEndpoint.post = openapi.body({'application/json': AuthSchema}, required=True)(AuthenticateEndpoint.post)
    openapi.response(200, {'application/json': AuthTokensSchema})(AuthenticateEndpoint.post)
    openapi.response(400, {'application/json': ResponseSchema})(AuthenticateEndpoint.post)
    openapi.response(401, {'application/json': AuthErrorSchema})(AuthenticateEndpoint.post)
    openapi.response(403, {'application/json': AuthErrorSchema})(AuthenticateEndpoint.post)
    openapi.response(500, {'application/json': ResponseSchema})(AuthenticateEndpoint.post)

    openapi.operation('getCurrentUser')(RetrieveUserEndpoint.get)
    openapi.summary('Get current user')(RetrieveUserEndpoint.get)
    openapi.secured(True)(RetrieveUserEndpoint.get)
    openapi.response(200, {'application/json': CurrentUserSchema})(RetrieveUserEndpoint.get)
    openapi.response(400, {'application/json': AuthErrorSchema})(RetrieveUserEndpoint.get)
    openapi.response(401, {'application/json': AuthErrorSchema})(RetrieveUserEndpoint.get)
    openapi.response(403, {'application/json': AuthErrorSchema})(RetrieveUserEndpoint.get)
    openapi.response(500, {'application/json': ResponseSchema})(RetrieveUserEndpoint.get)

    openapi.operation('checkAuthentication')(VerifyEndpoint.get)
    openapi.summary('Check authentication')(VerifyEndpoint.get)
    openapi.secured(True)(VerifyEndpoint.get)
    openapi.response(200, {'application/json': AuthVerifySchema})(VerifyEndpoint.get)
    openapi.response(400, {'application/json': AuthErrorSchema})(VerifyEndpoint.get)
    openapi.response(401, {'application/json': AuthErrorSchema})(VerifyEndpoint.get)
    openapi.response(403, {'application/json': AuthErrorSchema})(VerifyEndpoint.get)
    openapi.response(500, {'application/json': ResponseSchema})(VerifyEndpoint.get)

    openapi.operation('refreshAccessToken')(RefreshEndpoint.post)
    openapi.summary('Refresh access token')(RefreshEndpoint.post)
    openapi.secured(True)(RefreshEndpoint.post)
    RefreshEndpoint.post = openapi.body({'application/json': RefreshTokenSchema}, required=True)(RefreshEndpoint.post)
    openapi.response(200, {'application/json': AccessTokenSchema})(RefreshEndpoint.post)
    openapi.response(400, {'application/json': AuthErrorSchema})(RefreshEndpoint.post)
    openapi.response(401, {'application/json': AuthErrorSchema})(RefreshEndpoint.post)
    openapi.response(403, {'application/json': AuthErrorSchema})(RefreshEndpoint.post)
    openapi.response(500, {'application/json': ResponseSchema})(RefreshEndpoint.post)

    openapi.operation('logout')(LogoutEndpoint.post)
    openapi.summary('Logout')(LogoutEndpoint.post)
    openapi.secured(True)(LogoutEndpoint.post)
    openapi.response(200, {'application/json': ResponseSchema})(LogoutEndpoint.post)
    openapi.response(400, {'application/json': AuthErrorSchema})(LogoutEndpoint.post)
    openapi.response(401, {'application/json': AuthErrorSchema})(LogoutEndpoint.post)
    openapi.response(403, {'application/json': AuthErrorSchema})(LogoutEndpoint.post)
    openapi.response(500, {'application/json': ResponseSchema})(LogoutEndpoint.post)


class JWT(Initialize):
    def __init__(self, app: Sanic, **kwargs):
        super().__init__(
            instance=app,
            authenticate=authenticate,
            retrieve_user=retrieve_user,
            add_scopes_to_payload=scope_extender,
            store_refresh_token=store_refresh_token,
            retrieve_refresh_token=retrieve_refresh_token,
            class_views=[('/logout', LogoutEndpoint)],
            **kwargs
        )
        register_openapi_routes()
