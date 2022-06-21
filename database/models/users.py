from enum import Enum

from sqlalchemy.dialects.postgresql import ENUM

from .db import db
from .base_model import BaseModel

class UserRole(Enum):
    Admin = 'Admin'
    User = 'User'

class UserSubject(Enum):
    FizFace = 'Fiz'
    UrFace = 'Ur'

class User(BaseModel):
    __tablename__ = 'users'
    __hiden_keys__ = ('password')
    password = db.Column(db.String(), nullable=False)
    tel = db.Column(db.String(), nullable=False)

    role = db.Column(
        ENUM(UserRole,
        name='user_roles'),
        nullable=False,
        index=True, default=UserRole.User,
        server_default=UserRole.User.value,
        comment='User roles')

    subject = db.Column(
        ENUM(UserSubject,
        name='user_subject'),
        index=True, default=UserSubject.FizFace,
        server_default=UserSubject.FizFace.value,
        comment='User subject')
