import imp
import sqlalchemy
from gino import Gino
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func
from enum import Enum
from .db import db

class UserLang(Enum):
    EN = 'EN'
    RU = 'RU'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), default='noname')
    password = db.Column(db.String(), default='noname') #string
    image = db.Column(db.Unicode(), default='noname') #байт
    lang = db.Column(ENUM(UserLang, name='user_langs'), nullable=False, index=True, default=UserLang.EN, server_default=UserLang.EN.value, comment='User lang')  # noqa