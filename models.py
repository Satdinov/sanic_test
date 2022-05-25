import sqlalchemy
from gino import Gino
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


db= Gino()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), default='noname')
    password = db.Column(db.String(), default='noname') #string
    lang = db.Column(db.Unicode(), default='noname') #enum
    image = db.Column(db.Unicode(), default='noname') #байт
