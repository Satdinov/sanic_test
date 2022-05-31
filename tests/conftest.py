import os
from decimal import Decimal
from typing import Tuple

import aioredis
import pytest
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from gino import Gino
from pytest_postgresql.janitor import DatabaseJanitor
from sanic import Sanic
from sanic_testing import TestManager
from sqlalchemy.engine.url import make_url

from app.app import create_app
from app.config import Config
from app.extensions import register_jwt, register_password_hasher
from database import User, UserRole, db


@pytest.fixture
async def database() -> Gino:
    pg_connection = os.environ['SANIC_PG_CONNECTION']
    pg_version = os.environ['SANIC_PG_VERSION']

    pg_connection_url = make_url(pg_connection)
    janitor = DatabaseJanitor(
        user=pg_connection_url.username,
        password=pg_connection_url.password,
        host=pg_connection_url.host,
        port=pg_connection_url.port,
        dbname=pg_connection_url.database,
        version=pg_version
    )
    janitor.init()

    alembic_config = AlembicConfig(Config.ALEMBIC_INI_PATH)
    alembic_config.set_main_option('script_location', Config.ALEMBIC_SCRIPTS_PATH)
    alembic_config.set_main_option('sqlalchemy.url', pg_connection)
    alembic_upgrade(alembic_config, 'head')

    await db.set_bind(pg_connection, echo=False, min_size=5, max_size=10)

    yield db

    await db.pop_bind().close()
    janitor.drop()


@pytest.fixture
async def redis() -> aioredis.Redis:
    redis_connection = os.environ['SANIC_REDIS_CONNECTION']
    rdb = await aioredis.from_url(redis_connection)

    yield rdb

    await rdb.close()


@pytest.fixture
def app(database: Gino, redis: aioredis.Redis) -> Sanic:
    Config.TESTS = True
    sanic_app = create_app(config_object=Config, need_register_extensions=False)

    register_password_hasher(sanic_app)
    register_jwt(sanic_app)

    sanic_app.ctx.db = database
    sanic_app.ctx.redis = redis

    yield sanic_app


@pytest.fixture
def test_manager(app: Sanic) -> TestManager:
     return TestManager(app)


@pytest.fixture
def password() -> str:
    return 'password'


@pytest.fixture
async def hashed_password(app: Sanic, password: str) -> str:
    return await app.ctx.password_hasher.async_hash(password)


@pytest.fixture
def invalid_strings() -> Tuple[str]:
    return (1234, True, False, None)


@pytest.fixture
def invalid_ids() -> Tuple[str]:
    return ('invalid', '1234', 1234, True, False)


@pytest.fixture
def invalid_logins() -> Tuple[str]:
    return ('invalid', '1234', 1234, True, False, None)


@pytest.fixture
def invalid_passwords() -> Tuple[str]:
    return ('invalid', '1234', 1234, True, False, None)


@pytest.fixture
def invalid_otps() -> Tuple[str]:
    return ('invalid', '1234', 1234, True, False, None)


@pytest.fixture
async def admin(database: Gino, password: str, hashed_password: str) -> User:
    user = await User.create(
        role=UserRole.ADMIN,
        login='admin',
        password=hashed_password,
    )

    yield user

    await user.delete()


@pytest.fixture
async def user(database: Gino, password: str, hashed_password: str) -> User:
    user = await User.create(
        role=UserRole.USER,
        login='user',
        password=hashed_password,
    )

    yield user

    await user.delete()
