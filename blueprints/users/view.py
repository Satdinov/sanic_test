import imp
from sanic import Blueprint
from sanic.response import json, raw
from sanic_ext import openapi

from utils.openapi_models import ResponseSchema

from .models import AddUserSchema, ChangeEmailSchema
from database import User, loaders
from utils import dehash_pass, hash_pass, validate_email, validate_password


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
@openapi.body({"multipart/form-data": AddUserSchema}, required=True)
async def add_user(request):
    form = request.form
    all_users = await loaders.users_query().all()
    if validate_email(form['email'][0]) and validate_password(form['password'][0]):
        password = hash_pass(form['password'][0])
        user = await User.create(
            id = len(all_users)+1,
            email = form['email'][0],
            password = password,
            lang = form['lang'][0]
        )
    else:
        return json({'status':'400'})

    
    return json(user.to_dict())


@blueprint.patch("/change_email/<user_id>")
@openapi.body({"multipart/form-data": ChangeEmailSchema}, required=True)
async def change_user(request, user_id):
    form = request.form
    user = await loaders.users_query(user_id=int(user_id)).first()
    await user.update(email = form['email'][0]).apply()
    return json(user.to_dict())


@blueprint.delete("/delete_user/<user_id>")
async def delete_user(request, user_id):
    user = await loaders.users_query(user_id=int(user_id)).first()
    await user.delete()
    return json({'status':'200'})


@blueprint.get("/get_user/<user_id>")
async def get_user(request,user_id):
    user = await loaders.users_query(user_id=int(user_id)).first()
    return json(user.to_dict())



