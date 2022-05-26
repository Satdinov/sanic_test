import sys
import uuid
from base64 import b64encode
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Any, Dict

from gino.crud import CRUDModel as _CRUDModel


if 'sanic' in sys.modules:
    from gino.ext.sanic import Gino as _Gino  # pylint: disable=import-error
else:
    from gino import Gino as _Gino



class CRUDModel(_CRUDModel):
    hiden_keys = ()

    def _value_serializer(self, value: Any) -> Any:
        if isinstance(value, uuid.UUID):
            return str(value)
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, datetime):
            return value.isoformat(' ')
        if isinstance(value, timedelta):
            return value.total_seconds()
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, bytes):
            return b64encode(value).decode()
        if isinstance(value, list):
            return [self._value_serializer(item) for item in value]
        if isinstance(value, _CRUDModel):
            return value.to_dict()
        return value

    def to_dict(self, del_hiden_keys: bool = True) -> Dict:  # pylint: disable=arguments-differ
        data = {}
        for key in list(self.__dict__.get('__values__', {}).keys()) + list(self.__dict__.keys()):
            if key.startswith('_') or (del_hiden_keys and key in getattr(self, '__hiden_keys__', [])):
                continue
            data[key] = self._value_serializer(getattr(self, key, None))
        return data

class Gino(_Gino):
    model_base_classes = (CRUDModel,)

db = Gino()