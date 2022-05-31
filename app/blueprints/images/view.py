from sanic import Blueprint
from sanic.response import json, raw
from sanic_ext import openapi
from sanic_jwt.decorators import inject_user, protected, scoped

from database import User, Image, loaders, UserRole
from app.utils.openapi_models import ResponseSchema, AuthErrorSchema, UserSchema
from .models import AddImageSchema


blueprint = Blueprint('images', url_prefix='/images', strict_slashes=True)


@blueprint.post("/add_image/<user_id>")
@openapi.summary("Add image")
@openapi.description("Add user's images to database")
@openapi.response(200, {'application/json': UserSchema}, description='OK')
@openapi.response(400, {'application/json': ResponseSchema}, description='Bad Request')
@openapi.response(401, {'application/json': AuthErrorSchema}, description='Unauthorized')
@openapi.response(403, {'application/json': AuthErrorSchema}, description='Forbidden')
@openapi.response(404, {'application/json': ResponseSchema}, description='Not Found')
@openapi.response(500, {'application/json': ResponseSchema}, description='Internal Server Error')
@openapi.body({"multipart/form-data": AddImageSchema}, required=True)
@protected()
@inject_user()
@scoped((UserRole.Admin.value, UserRole.User.value,), require_all=False)
async def add_image(request, user_id, user: User):
    if user.role != UserRole.Admin.value:
        user_id = str(user.id)
    user = await loaders.users_query(user_id=int(user_id)).first_or_404()
    image = await loaders.image_query(user_id=user.id).first()
    file = request.files['image'][0]

    if not image:
        await Image.create(
            user_id=int(user_id),
            image=file.body,
            image_mime_type=file.type)

    else:
        await image.update(
            image=file.body,
            image_mime_type=file.type
        ).apply()
    return json({'status': 200})


@blueprint.get("/get_image/<user_id>")
@openapi.summary("Get image")
@openapi.description("Get user's image from database")
@openapi.response(200, {'application/json': UserSchema}, description='OK')
@openapi.response(400, {'application/json': ResponseSchema}, description='Bad Request')
@openapi.response(401, {'application/json': AuthErrorSchema}, description='Unauthorized')
@openapi.response(403, {'application/json': AuthErrorSchema}, description='Forbidden')
@openapi.response(404, {'application/json': ResponseSchema}, description='Not Found')
@openapi.response(500, {'application/json': ResponseSchema}, description='Internal Server Error')
@protected()
@inject_user()
@scoped((UserRole.Admin.value, UserRole.User.value,), require_all=False)
async def get_image(request, user_id, user: User):  # pylint: disable=unused-argument
    if user.role != UserRole.Admin.value:
        user_id = str(user.id)
    image = await loaders.image_query(user_id=int(user_id)).first_or_404()
    return raw(image.image, content_type=image.image_mime_type)
