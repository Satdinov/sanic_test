import aioredis
from sanic import Blueprint, Sanic

import blueprints
from database import db
from utils import jwt, password_hasher

from config import Config


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


app = Sanic(Config.APP_NAME)

app.config.load(Config)
app.config.load_environment_vars()

def register_db(app: Sanic):
    app.config.DB_DSN = app.config.PG_CONNECTION
    db.init_app(app)
    app.ctx.db = db

def register_blueprints(app: Sanic):
    app.blueprint(Blueprint.group(
        blueprints.images.blueprint,
        blueprints.users.blueprint,
    ))


def register_extensions(app: Sanic):
    register_jwt(app)
    register_password_hasher(app)
    register_redis(app)
    register_blueprints(app)
    register_db(app)

register_extensions(app)