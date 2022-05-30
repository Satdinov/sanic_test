from datetime import datetime
from enum import Enum
from typing import Optional

from gino import Gino
from gino.api import GinoExecutor

from ..models import Image

# поиск по атрибутам в БД
def image_query(
    user_id_im: Optional[str] = None,
) -> GinoExecutor:

    query = Image.query

    if user_id_im:
        query = query.where(Image.user_id == user_id_im)

    return query.gino