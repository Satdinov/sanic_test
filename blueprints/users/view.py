from sanic import Blueprint
from sanic.response import json
from sanic_ext import openapi, validate
from sanic_jwt.decorators import inject_user, protected, scoped

from database import User, loaders, UserRole
from utils import PasswordHasher
from utils.openapi_models import ResponseSchema, UserSchema, AuthErrorSchema

from .models import AddUserModel, AddUserSchema, ChangeEmailSchema


blueprint = Blueprint('users', url_prefix='/users', strict_slashes=True)


@blueprint.get("/get_users")
@openapi.summary("Get users")
@openapi.description("Get users from database")
@openapi.response(200, {'application/json': UserSchema}, description='OK')
@openapi.response(400, {'application/json': ResponseSchema}, description='Bad Request')
@openapi.response(401, {'application/json': AuthErrorSchema}, description='Unauthorized')
@openapi.response(403, {'application/json': AuthErrorSchema}, description='Forbidden')
@openapi.response(404, {'application/json': ResponseSchema}, description='Not Found')
@openapi.response(500, {'application/json': ResponseSchema}, description='Internal Server Error')
@scoped((UserRole.Admin.value, ), require_all=False)
@protected()
async def get_users(request):  # pylint: disable=unused-argument
    all_users = await loaders.users_query().all()
    return json([user.to_dict() for user in all_users])


@blueprint.post("/add_user")
@openapi.summary("Add user")
@openapi.description("Add user to database")
@openapi.response(200, {'application/json': UserSchema}, description='OK')
@openapi.response(400, {'application/json': ResponseSchema}, description='Bad Request')
@openapi.response(401, {'application/json': AuthErrorSchema}, description='Unauthorized')
@openapi.response(403, {'application/json': AuthErrorSchema}, description='Forbidden')
@openapi.response(404, {'application/json': ResponseSchema}, description='Not Found')
@openapi.response(500, {'application/json': ResponseSchema}, description='Internal Server Error')
@openapi.body({"application/json": AddUserSchema}, required=True)
@validate(json=AddUserModel)
async def add_user(request, body):  # pylint: disable=unused-argument
    body.email = body.email.lower()
    user = await loaders.users_query(email=body.email).first()
    if not user:
        password_hasher = PasswordHasher()
        password = await password_hasher.async_hash(body.password)
        user = await User.create(
            email=body.email,
            password=password,
            lang=body.lang,
            role=body.role
        )
    else:
        return json({'status': '400'})
    return json(user.to_dict())


@blueprint.patch("/change_email/<user_id>")
@openapi.summary("Change email")
@openapi.description("Change email from user")
@openapi.response(200, {'application/json': UserSchema}, description='OK')
@openapi.response(400, {'application/json': ResponseSchema}, description='Bad Request')
@openapi.response(401, {'application/json': AuthErrorSchema}, description='Unauthorized')
@openapi.response(403, {'application/json': AuthErrorSchema}, description='Forbidden')
@openapi.response(404, {'application/json': ResponseSchema}, description='Not Found')
@openapi.response(500, {'application/json': ResponseSchema}, description='Internal Server Error')
@openapi.body({"application/json": ChangeEmailSchema}, required=True)
@protected()
@inject_user()
@scoped((UserRole.Admin.value, UserRole.User.value,), require_all=False)
async def change_user(request, user_id, user:User):
    if user.role != UserRole.Admin.value:
        user_id = str(user.id)
    form = request.form
    user = await loaders.users_query(user_id=int(user_id)).first_or_404()
    await user.update(email=form['email'][0]).apply()
    return json(user.to_dict())


@blueprint.delete("/delete_user/<user_id>")
@openapi.summary("Delete user")
@openapi.description("Delete user from database")
@openapi.response(200, {'application/json': UserSchema}, description='OK')
@openapi.response(400, {'application/json': ResponseSchema}, description='Bad Request')
@openapi.response(401, {'application/json': AuthErrorSchema}, description='Unauthorized')
@openapi.response(403, {'application/json': AuthErrorSchema}, description='Forbidden')
@openapi.response(404, {'application/json': ResponseSchema}, description='Not Found')
@openapi.response(500, {'application/json': ResponseSchema}, description='Internal Server Error')
@protected()
@scoped((UserRole.Admin.value, UserRole.User.value,), require_all=False)
@inject_user()
async def delete_user(request, user_id, user:User):  # pylint: disable=unused-argument
    if user.role != UserRole.Admin.value:
        user_id = str(user.id)
    user = await loaders.users_query(user_id=int(user_id)).first_or_404()
    await user.delete()
    return json({'status': '200'})


@blueprint.get("/get_user/<user_id>")
@openapi.summary("Get user")
@openapi.description("Get user from database")
@openapi.response(200, {'application/json': UserSchema}, description='OK')
@openapi.response(400, {'application/json': ResponseSchema}, description='Bad Request')
@openapi.response(401, {'application/json': AuthErrorSchema}, description='Unauthorized')
@openapi.response(403, {'application/json': AuthErrorSchema}, description='Forbidden')
@openapi.response(404, {'application/json': ResponseSchema}, description='Not Found')
@openapi.response(500, {'application/json': ResponseSchema}, description='Internal Server Error')
@protected()
@inject_user()
@scoped((UserRole.Admin.value, UserRole.User.value,), require_all=False)
async def get_user(request, user_id, user:User):  # pylint: disable=unused-argument
    if user.role != UserRole.Admin.value:
        user_id = str(user.id)
    user = await loaders.users_query(user_id=int(user_id)).first_or_404()
    return json(user.to_dict())
