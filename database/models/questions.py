from .db import db

from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM
from .base_model import BaseModel

class Questions(BaseModel):
    __tablename__ = 'questions'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='User ID')  # noqa
    comment = db.Column(db.String(), nullable=False)
