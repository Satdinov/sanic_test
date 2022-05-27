from enum import Enum
from typing import Dict

from .db import db

class Image(db.Model):
    __tablename__ = 'image_data'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='User ID')  # noqa
    image = db.Column(db.LargeBinary())
    image_mime_type = db.Column(db.String())