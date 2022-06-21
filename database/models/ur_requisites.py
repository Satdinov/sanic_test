from .db import db
from .base_model import BaseModel


class Ur_Requisites(BaseModel):
    __tablename__ = 'ur_requisites_data'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='User ID')  # noqa
    FIO = db.Column(db.String(), nullable=False)
    org_name = db.Column(db.String(), nullable=False)
    INN = db.Column(db.Integer(), nullable=False)
    KPP = db.Column(db.Integer(), nullable=False)
    OGRN = db.Column(db.Integer(), nullable=False)
    BIK = db.Column(db.Integer(), nullable=False)
    payment_number = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    tel = db.Column(db.String(), nullable=False)
    address = db.Column(db.String())
    delivery = db.Column(db.String())

