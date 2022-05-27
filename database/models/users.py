from enum import Enum
from typing import Dict

from sqlalchemy.dialects.postgresql import ENUM

from .db import db


class UserLang(Enum):
    EN = 'EN'
    RU = 'RU'

class UserRole(Enum):
    Admin = 'Admin'
    User = 'User'

class User(db.Model):
    __tablename__ = 'users'
    __hiden_keys__ = ('image','password', 'image_mime_type')
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), default='noname')
    password = db.Column(db.String(), default='noname') #string
    lang = db.Column(ENUM(UserLang, name='user_langs'), nullable=False, index=True, default=UserLang.EN, server_default=UserLang.EN.value, comment='User lang')  # noqa
    role = db.Column(ENUM(UserRole, name='user_roles'), nullable=False, index=True, default=UserRole.User, server_default=UserRole.User.value, comment='User roles')  # noqa

