from .db import db
from .base_model import BaseModel


class Fiz_Requisites(BaseModel):
    __tablename__ = 'fiz_requisites_data'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='User ID')  # noqa
    FIO = db.Column(db.String(), nullable=False)
    series_passport = db.Column(db.Integer())
    number_passport = db.Column(db.Integer())
    email = db.Column(db.String(), nullable=False)
    tel = db.Column(db.String(), nullable=False)
    delivery = db.Column(db.String())
