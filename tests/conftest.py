import os
from decimal import Decimal
from typing import Tuple

import aioredis
import pytest
import asyncio
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from gino import Gino
from pytest_postgresql.janitor import DatabaseJanitor
from sanic import Sanic
from sanic_testing import TestManager
from sqlalchemy.engine.url import make_url

from app.app import create_app
from app.config import Config
from app.app import register_jwt, register_password_hasher
from database import User, UserLang, UserRole, db


@pytest.fixture
async def database():
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
    #breakpoint()
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
    return 'password1'


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
def invalid_emails() -> Tuple[str]:
    return ('invalid', '1234', 1234, True, False, None)


@pytest.fixture
def invalid_passwords() -> Tuple[str]:
    return ('invalid', '1234', 1234, True, False, None)


@pytest.fixture
async def user(app: Sanic, database: Gino, password: str, hashed_password: str) -> User:
    async with app.ctx.db.transaction():
        user = await User.create(
            email='user@user.com',
            password=hashed_password,  
            lang=UserLang.EN,
            role=UserRole.User,
        )
        user._raw_password = password
    yield user

    await user.delete()

@pytest.fixture
async def admin(app: Sanic, database: Gino, password: str, hashed_password: str) -> User:
    async with app.ctx.db.transaction():
        user = await User.create(
            email='admin@admin.com',
            password=hashed_password,
            role=UserRole.Admin,
            lang=UserLang.EN,
        )
        user._raw_password = password
    yield user

    await user.delete()

'''
@pytest.fixture
async def rank(database: Gino) -> Rank:
    rank = await Rank.create(
        name='Initial',
        min_usd_deposit=None,
        max_usd_deposit=Decimal('100'),
        linear_profits=[Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0')]
    )

    yield rank

    await rank.delete()


@pytest.fixture
async def admin(app: Sanic, database: Gino, password: str, hashed_password: str, rank: Rank) -> User:
    async with app.ctx.db.transaction():
        user = await User.create(
            referral_link_id=None,
            role=UserRole.ADMIN,
            lang=UserLang.EN,
            rank_id=rank.id,
            email='admin@admin.com',
            password=hashed_password,
            firstname='admin',
            lastname='admin',
            is_email_verified=True,
            image=b'image',
            image_mime_type='image/png'
        )
        user._raw_password = password
        user.rank = rank
        # user.total_usd_deposit = await user.usd_deposit()
        # user.total_week_usd_withdraw = await user.week_usd_withdraw()

    yield user

    await user.delete()


@pytest.fixture
async def admin_referral_link(database: Gino, admin: User) -> ReferralLink:
    referral_link = await ReferralLink.create(user_id=admin.id)
    referral_link.user = admin

    yield referral_link

    await referral_link.delete()


@pytest.fixture
async def user(app: Sanic, database: Gino, password: str, hashed_password: str, rank: Rank, admin_referral_link: ReferralLink) -> User:
    async with app.ctx.db.transaction():
        user = await User.create(
            referral_link_id=admin_referral_link.id,
            role=UserRole.USER,
            lang=UserLang.EN,
            rank_id=rank.id,
            email='user@user.com',
            password=hashed_password,
            firstname='user',
            lastname='user',
            is_email_verified=True,
            image=b'image',
            image_mime_type='image/png'
        )
        user._raw_password = password
        user.rank = rank
        # user.total_usd_deposit = await user.usd_deposit()
        # user.total_week_usd_withdraw = await user.week_usd_withdraw()
    yield user

    await user.delete()


@pytest.fixture
async def user_referral_link(database: Gino, user: User) -> ReferralLink:
    referral_link = await ReferralLink.create(user_id=user.id)
    referral_link.user = user

    yield referral_link

    await referral_link.delete()


@pytest.fixture
async def partner(database: Gino, password: str, hashed_password: str, rank: Rank, user_referral_link: ReferralLink) -> User:
    user = await User.create(
        referral_link_id=user_referral_link.id,
        role=UserRole.USER,
        lang=UserLang.EN,
        rank_id=rank.id,
        email='partner@partner.com',
        password=hashed_password,
        firstname='partner',
        lastname='partner',
        is_email_verified=True,
        image=b'image',
        image_mime_type='image/png'
    )
    user._raw_password = password
    user.rank = rank

    yield user

    await user.delete()


@pytest.fixture
async def admin_with_otp(database: Gino, password: str, hashed_password: str, rank: Rank) -> User:
    user = await User.create(
        referral_link_id=None,
        role=UserRole.ADMIN,
        lang=UserLang.EN,
        rank_id=rank.id,
        email='admin_otp@admin.com',
        password=hashed_password,
        firstname='admin_otp',
        lastname='admin_otp',
        is_email_verified=True,
        is_2fa_enabled=True
    )
    user._raw_password = password
    user.rank = rank

    yield user

    await user.delete()


@pytest.fixture
async def user_with_otp(database: Gino, password: str, hashed_password: str, rank: Rank) -> User:
    user = await User.create(
        referral_link_id=None,
        role=UserRole.USER,
        lang=UserLang.EN,
        rank_id=rank.id,
        email='user_otp@user.com',
        password=hashed_password,
        firstname='user_otp',
        lastname='user_otp',
        is_email_verified=True,
        is_2fa_enabled=True
    )
    user._raw_password = password
    user.rank = rank

    yield user

    await user.delete()


@pytest.fixture
async def network(database: Gino) -> Network:
    network = await Network.create(
        name='Binance Smart Chain',
        bip='BIP44',
        python_class='EthereumMainnet',
        has_web3=True,
        web3_rpc_url='https://bsc-dataseed.binance.org/'
    )

    yield network

    await network.delete()


@pytest.fixture
async def coin_busd(database: Gino, network: Network) -> Coin:
    coin = await Coin.create(
        network_id=network.id,
        name='Binance USD',
        symbol='BUSD',
        is_token=True,
        is_stable=True,
        depositable=True,
        withdrawable=False,
        address='0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56',
        logo_url='https://raw.githubusercontent.com/trustwallet/assets/master/blockchains/smartchain/assets/0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56/logo.png'  # noqa
    )
    coin.network = network

    yield coin

    await coin.delete()


@pytest.fixture
async def coin_mfx(database: Gino, network: Network) -> Coin:
    coin = await Coin.create(
        network_id=network.id,
        name='MetaFerma',
        symbol='MFX',
        is_token=True,
        is_stable=False,
        depositable=True,
        withdrawable=False,
        address='0xF78D45Fd75cb339B1123776f6C349123deF0aB75',
        logo_url=None
    )
    coin.network = network

    yield coin

    await coin.delete()


@pytest.fixture
async def coin_pair_busd_mfx(database: Gino, coin_busd: Coin, coin_mfx: Coin) -> CoinPair:
    coin_pair = await CoinPair.create(
        from_coin_id=coin_busd.id,
        to_coin_id=coin_mfx.id,
        exchange_rate=Decimal('2.0'),
        exchange_liquidity=Decimal('100.0')
    )

    yield coin_pair

    await coin_pair.delete()


@pytest.fixture
async def admin_balance_busd(database: Gino, admin: User, coin_busd: Coin) -> Balance:
    balance = await Balance.create(
        user_id=admin.id,
        coin_id=coin_busd.id,
        amount=Decimal('100.0')
    )

    yield balance

    await balance.delete()


@pytest.fixture
async def user_balance_busd(database: Gino, user: User, coin_busd: Coin) -> Balance:
    balance = await Balance.create(
        user_id=user.id,
        coin_id=coin_busd.id,
        amount=Decimal('100.0')
    )

    yield balance

    await balance.delete()


@pytest.fixture
async def admin_balance_mfx(database: Gino, admin: User, coin_mfx: Coin) -> Balance:
    balance = await Balance.create(
        user_id=admin.id,
        coin_id=coin_mfx.id,
        amount=Decimal('100.0')
    )

    yield balance

    await balance.delete()


@pytest.fixture
async def user_balance_mfx(database: Gino, user: User, coin_mfx: Coin) -> Balance:
    balance = await Balance.create(
        user_id=user.id,
        coin_id=coin_mfx.id,
        amount=Decimal('100.0')
    )

    yield balance

    await balance.delete()


@pytest.fixture
async def admin_balance_operation_busd(database: Gino, admin_balance_busd: Balance) -> BalanceOperation:
    balance_operation = await BalanceOperation.create(
        balance_id=admin_balance_busd.id,
        type=BalanceOperationType.DEPOSIT,
        amount=Decimal('100.0'),
        usd_rate=Decimal('1')
    )

    yield balance_operation

    await balance_operation.delete()


@pytest.fixture
async def user_balance_operation_busd(database: Gino, user_balance_busd: Balance) -> BalanceOperation:
    balance_operation = await BalanceOperation.create(
        balance_id=user_balance_busd.id,
        type=BalanceOperationType.DEPOSIT,
        amount=Decimal('100.0'),
        usd_rate=Decimal('1')
    )

    yield balance_operation

    await balance_operation.delete()


@pytest.fixture
async def admin_balance_operation_mfx(database: Gino, admin_balance_mfx: Balance) -> BalanceOperation:
    balance_operation = await BalanceOperation.create(
        balance_id=admin_balance_mfx.id,
        type=BalanceOperationType.DEPOSIT,
        amount=Decimal('100.0'),
        usd_rate=Decimal('1')
    )

    yield balance_operation

    await balance_operation.delete()


@pytest.fixture
async def user_balance_operation_mfx(database: Gino, user_balance_mfx: Balance) -> BalanceOperation:
    balance_operation = await BalanceOperation.create(
        balance_id=user_balance_mfx.id,
        type=BalanceOperationType.DEPOSIT,
        amount=Decimal('10.0'),
        usd_amount=Decimal('10.0')
    )

    yield balance_operation

    await balance_operation.delete()


@pytest.fixture
async def admin_support_ticket(database: Gino, admin: User) -> SupportTicket:
    support_ticket = await SupportTicket.create(
        user_id=admin.id,
        email=admin.email,
        name=f'{admin.firstname} {admin.lastname}',
        message='message'
    )

    yield support_ticket

    await support_ticket.delete()


@pytest.fixture
async def user_support_ticket(database: Gino, user: User) -> SupportTicket:
    support_ticket = await SupportTicket.create(
        user_id=user.id,
        email=user.email,
        name=f'{user.firstname} {user.lastname}',
        message='message'
    )

    yield support_ticket

    await support_ticket.delete()


@pytest.fixture
async def test_db_alembic_config() -> AlembicConfig:
    config = AlembicConfig()

    return
'''
