from datetime import datetime
from enum import Enum
from typing import Optional
from gino.api import GinoExecutor
from ..models import User,UserLang
from gino import Gino
from ..models import db


# поиск по атрибутам в БД
def users_query(
    user_id: Optional[str] = None,
    email: Optional[str] = None,
    lang: Optional[UserLang] = None,
    is_deleted: bool = None,
) -> GinoExecutor:

    query = User.query

    if user_id:
        query = query.where(User.id == user_id)

    if email:
        query = query.where(User.email == email)

    if lang:
        query = query.where(User.lang == lang)


    return query.gino
