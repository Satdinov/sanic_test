from sanic import Blueprint
from sanic.response import json, raw

from database import User, loaders
from utils import dehash_pass, hash_pass, validate_email, validate_password


blueprint = Blueprint('api', url_prefix='/api', strict_slashes=True)

@blueprint.get("/get_users")
async def get_users(request):
    all_users = await loaders.users_query().all()
    return json([user.to_dict() for user in all_users])


@blueprint.post("/add_user")
async def add_user(request):
    form = request.form
    file = request.files['image'][0]
    body= file.body
    type = file.type
    all_users = await loaders.users_query().all()

    if validate_email(form['email'][0]) and validate_password(form['password'][0]):
        password = hash_pass(form['password'][0])
        user = await User.create(
            id = len(all_users)+1,
            email = form['email'][0],
            password = password,
            lang = 'RU',
            image = body,
            image_mime_type = type)
    else:
        return json({'status':'400'})

    
    return json(user.to_dict())


@blueprint.patch("/change_email/<user_id>")
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


@blueprint.get("/get_image/<user_id>")
async def get_image(request,user_id):
    user = await loaders.users_query(user_id=int(user_id)).first()
    return raw(user.image, content_type=user.image_mime_type)
