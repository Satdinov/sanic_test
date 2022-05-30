from typing import Optional

from gino.api import GinoExecutor

from ..models import Image


# поиск по атрибутам в БД
def image_query(
    user_id: Optional[int] = None,
    image_id: Optional[int] = None,
) -> GinoExecutor:

    query = Image.query

    if user_id:
        query = query.where(Image.user_id == user_id)

    if image_id:
        query = query.where(Image.id == image_id)

    return query.gino
