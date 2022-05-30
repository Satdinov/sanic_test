from sanic_ext.extensions.openapi.types import Schema


class AddImageSchema:
    image = Schema(type='file', description='User file',
                  required=True, nullable=False)
