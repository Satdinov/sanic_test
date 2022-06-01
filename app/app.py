import aio_pika
import aioredis
from sanic import Blueprint, Sanic

from . import blueprints
from database import db
from app.utils import jwt, password_hasher

from . import config


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

''''
app = Sanic(Config.APP_NAME)

app.config.load(Config)
app.config.load_environment_vars()
'''
def create_app(config_object: object = config.Config, need_register_extensions: bool = True) -> Sanic:
    app = Sanic(config_object.APP_NAME)
    app.config.load(config_object)
    app.config.load_environment_vars()
    if need_register_extensions:
        register_extensions(app)
    register_blueprints(app)
    return app

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
    register_rabbitmq(app)

def register_rabbitmq(app: Sanic):

    async def create_amqp_connection(app: Sanic, _):
        app.ctx.amqp = await aio_pika.connect_robust(app.config.AMQP_CONNECTION)
        app.ctx.amqp_channel = await app.ctx.amqp.channel()
    
    app.register_listener(create_amqp_connection, 'before_server_start')
