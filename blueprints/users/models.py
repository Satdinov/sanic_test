from sanic_ext import openapi

class AddUserSchema:
    email = openapi.String(description='User email')
    password = openapi.String(description='User password')
    lang = openapi.String(description='User language')