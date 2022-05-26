from sqlalchemy.dialects.postgresql import ENUM
from typing import Dict
from enum import Enum
from .db import db

class UserLang(Enum):
    EN = 'EN'
    RU = 'RU'

class User(db.Model):
    __tablename__ = 'users'
    ___hiden_keys__ = ('image')
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), default='noname')
    password = db.Column(db.String(), default='noname') #string
    image = db.Column(db.LargeBinary())
    image_mime_type = db.Column(db.String())
    lang = db.Column(ENUM(UserLang, name='user_langs'), nullable=False, index=True, default=UserLang.EN, server_default=UserLang.EN.value, comment='User lang')  # noqa
