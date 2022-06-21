from .db import db

from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM
from .base_model import BaseModel


class Order_Status(Enum):
    Processing = 'Processing'  # В обработке
    Accepted = 'Accepted'  # Принят
    Confirmed = 'Confirmed'  # Подтвержден
    Operation = 'Operation'  # В работе
    Sent = 'Sent'  # Отправлен
    Completed = 'Completed'  # Выполнен

class Works(Enum):
    design = 'Design'  # Проектирование
    soldering = 'Soldering'  # Пайка
    revision = 'Revision'  # Доработка

class Orders(BaseModel):
    __tablename__ = 'orders'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='User ID')  # noqa
    name_order = db.Column(db.String())


    status = db.Column(
        ENUM(Order_Status,
        name='order_status'),
        nullable=False,
        index=True, default=Order_Status.Processing,
        server_default=Order_Status.Processing.value,
        comment='Order Status')

    orders_works = db.Column(
        ENUM(Works,
        name='works'),
        nullable=False,
        index=True, default=Works.soldering,
        server_default=Works.soldering.value,
        comment="Сustomer\'s work")

    comment = db.Column(db.String())
    file = db.Column(db.LargeBinary())
    file_type = db.Column(db.String())
