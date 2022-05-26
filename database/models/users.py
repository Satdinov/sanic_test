from sqlalchemy.dialects.postgresql import ENUM
from typing import Dict
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


    def to_dict(self, del_hiden_keys: bool = True) -> Dict:  # pylint: disable=arguments-differ
        data = super().to_dict(del_hiden_keys)
        return data