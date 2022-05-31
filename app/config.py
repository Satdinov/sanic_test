from typing import Tuple


app_name = 'sanic_test'


class Config:
    APP_NAME: str = app_name
    PG_CONNECTION: str = None
    REDIS_CONNECTION: str = None
    CORS_AUTOMATIC_OPTIONS: bool = True
    CORS_SUPPORTS_CREDENTIALS: bool = True
    CORS_ORIGINS: str = '.*'
    APP_URL_PREFIX: str = '/api'
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
    SANIC_JWT_URL_PREFIX: str = f'{APP_URL_PREFIX}/{SANIC_JWT_BLUEPRINT_NAME}'
    SANIC_JWT_COOKIE_SET: bool = True
    SANIC_JWT_COOKIE_STRICT: bool = False
    SANIC_JWT_EXPIRATION_DELTA: int = 7 * 24 * 60 * 60
    SANIC_JWT_USER_ID: str = 'id'
    SANIC_JWT_REFRESH_TOKEN_ENABLED: bool = False
