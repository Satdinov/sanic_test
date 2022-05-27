from tokenize import PseudoExtras
from sanic import Blueprint
from sanic.response import json, raw
from sanic_ext import openapi, validate
from utils.openapi_models import ResponseSchema

from .models import AddUserSchema, ChangeEmailSchema, AddUserModel
from database import User, loaders
from utils import dehash_pass, hash_pass, password_hasher, validate_email, validate_password, PasswordHasher

blueprint = Blueprint('users', url_prefix='/users', strict_slashes=True)

@blueprint.get("/get_users")
@openapi.summary("Get users")
@openapi.description("Get users from database")
@openapi.response(200, {'application/json': ResponseSchema}, description='OK')
@openapi.response(500, {'application/json': ResponseSchema}, description='Internal Server Error')
async def get_users(request):
    all_users = await loaders.users_query().all()
    return json([user.to_dict() for user in all_users])


@blueprint.post("/add_user")
@openapi.summary("Add user")
@openapi.description("Add user to database")
@openapi.response(200, {'application/json': ResponseSchema}, description='OK')
@openapi.response(500, {'application/json': ResponseSchema}, description='Internal Server Error')
@openapi.body({"application/json": AddUserSchema}, required=True)
@validate(json=AddUserModel)
async def add_user(request, body):
    all_users = await loaders.users_query().all()
    if validate_email(body.email) and validate_password(body.password):
        password_hasher = PasswordHasher()
        password = await password_hasher.async_hash(body.password)
        user = await User.create(
            id = len(all_users)+1,
            email = body.email,
            password = password,
            lang = body.lang,
            role = body.role
        )
    else:
        return json({'status':'400'})

    
    return json(user.to_dict())


@blueprint.patch("/change_email/<user_id>")
@openapi.summary("Change email")
@openapi.description("Change email from user")
@openapi.response(200, {'application/json': ResponseSchema}, description='OK')
@openapi.response(500, {'application/json': ResponseSchema}, description='Internal Server Error')
@openapi.body({"multipart/form-data": ChangeEmailSchema}, required=True)
async def change_user(request, user_id):
    form = request.form
    user = await loaders.users_query(user_id=int(user_id)).first()
    await user.update(email = form['email'][0]).apply()
    return json(user.to_dict())


@blueprint.delete("/delete_user/<user_id>")
@openapi.summary("Delete user")
@openapi.description("Delete user from database")
@openapi.response(200, {'application/json': ResponseSchema}, description='OK')
@openapi.response(500, {'application/json': ResponseSchema}, description='Internal Server Error')
async def delete_user(request, user_id):
    user = await loaders.users_query(user_id=int(user_id)).first()
    await user.delete()
    return json({'status':'200'})


@blueprint.get("/get_user/<user_id>")
@openapi.summary("Get user")
@openapi.description("Get user from database")
@openapi.response(200, {'application/json': ResponseSchema}, description='OK')
@openapi.response(500, {'application/json': ResponseSchema}, description='Internal Server Error')
async def get_user(request,user_id):
    user = await loaders.users_query(user_id=int(user_id)).first()
    return json(user.to_dict())



