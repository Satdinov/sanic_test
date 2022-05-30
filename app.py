from sanic import Blueprint, Sanic

from blueprints import users
import blueprints
from database import db
from utils import jwt, password_hasher
import aioredis
from typing import Tuple

def register_jwt(app: Sanic):
    app.ctx.jwt = jwt.JWT(app)
    app.ext.openapi.add_security_scheme(
        'token', 'http', scheme='bearer', bearer_format='JWT')

def register_password_hasher(app: Sanic):
    app.ctx.password_hasher = password_hasher.PasswordHasher()

def register_redis(app: Sanic):
    async def create_redis_connection(app: Sanic, _):
        app.ctx.redis = await aioredis.from_url(app.config.REDIS_CONNECTION)

    async def close_redis_connection(app: Sanic, _):
        if hasattr(app.ctx, 'redis'):
            await app.ctx.redis.close()

    app.register_listener(create_redis_connection, 'before_server_start')
    app.register_listener(close_redis_connection, 'before_server_stop')

app = Sanic('myapp')
app_name = 'sanic_test'

class Config:
    PG_CONNECTION: str = None
    REDIS_CONNECTION: str = None
    CORS_AUTOMATIC_OPTIONS: bool = True
    CORS_SUPPORTS_CREDENTIALS: bool = True
    CORS_ORIGINS: str = '.*'
    APP_URL_PREFIX: str = '/api'
    CORS_ALLOW_HEADERS: Tuple[str] = (
        'accept',
        'accept-encoding',
        'authorization',
        'content-type',
        'dnt',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with'
    )
    CORS_SEND_WILDCARD: bool = False

    SANIC_JWT_SECRET: str = f'{app_name} jwt super-super secret'
    SANIC_JWT_STRICT_SLASHES: bool = True
    SANIC_JWT_PATH_TO_AUTHENTICATE: str = ''
    SANIC_JWT_BLUEPRINT_NAME: str = 'auth'
    SANIC_JWT_URL_PREFIX: str = f'{APP_URL_PREFIX}/{SANIC_JWT_BLUEPRINT_NAME}'
    SANIC_JWT_COOKIE_SET: bool = True
    SANIC_JWT_COOKIE_STRICT: bool = False
    SANIC_JWT_EXPIRATION_DELTA: int = 7 * 24 * 60 * 60
    SANIC_JWT_USER_ID: str = 'id'
    SANIC_JWT_REFRESH_TOKEN_ENABLED: bool = False

app.config.load(Config)
app.config.load_environment_vars()

app.config.DB_DSN = app.config.PG_CONNECTION
db.init_app(app)
app.ctx.db = db

app.blueprint(Blueprint.group(
    blueprints.image.blueprint,
    blueprints.users.blueprint,
    #url_prefix=app.config.APP_URL_PREFIX
))

register_jwt(app)
register_password_hasher(app)
register_redis(app)