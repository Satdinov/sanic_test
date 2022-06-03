import os
from typing import Tuple


app_name = 'sanic_test'
app_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(app_dir, os.pardir))


class Config:
    APP_NAME: str = app_name
    # APP_URL_PREFIX: str = '/api'
    PG_CONNECTION: str = None
    REDIS_CONNECTION: str = None
    CORS_AUTOMATIC_OPTIONS: bool = True
    CORS_SUPPORTS_CREDENTIALS: bool = True
    CORS_ORIGINS: str = '.*'
    TESTS: bool = False
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
    # SANIC_JWT_URL_PREFIX: str = f'{APP_URL_PREFIX}/{SANIC_JWT_BLUEPRINT_NAME}'
    SANIC_JWT_URL_PREFIX: str = f'{SANIC_JWT_BLUEPRINT_NAME}'
    SANIC_JWT_COOKIE_SET: bool = True
    SANIC_JWT_COOKIE_STRICT: bool = False
    SANIC_JWT_EXPIRATION_DELTA: int = 7 * 24 * 60 * 60
    SANIC_JWT_USER_ID: str = 'id'
    SANIC_JWT_REFRESH_TOKEN_ENABLED: bool = False
    IMAGE_EXCHANGE: str = 'IMAGE_EXCHANGE'
    ALEMBIC_INI_PATH: str = os.path.join(project_root, 'database', 'alembic.ini')
    ALEMBIC_SCRIPTS_PATH: str = os.path.join(project_root, 'database', 'alembic')
