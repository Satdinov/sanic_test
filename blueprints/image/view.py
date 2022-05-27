from email.mime import image
from sanic import Blueprint
from sanic.response import json, raw
from sanic_ext import openapi

from database import Image, loaders
from utils import dehash_pass, hash_pass, validate_email, validate_password

from .models import AddImageSchema

blueprint = Blueprint('images', url_prefix='/images', strict_slashes=True)

@blueprint.get("/get_images")
async def get_images(request):
    all_images = await loaders.image_query().all()
    return json([image.to_dict() for image in all_images])

@blueprint.post("/add_image/<user_id>")
@openapi.body({"multipart/form-data": AddImageSchema}, required=True)
async def add_image(request, user_id):
    all_images = await loaders.image_query().all()
    file = request.files['image'][0]
    body= file.body
    type = file.type
    image = await Image.create(
        user_id = int(user_id),
        image = body,
        image_mime_type = type)
    return json(image.to_dict())

@blueprint.get("/get_image/<user_id>")
async def get_image(request,user_id):
    #user = await loaders.users_query(user_id=int(user_id)).first()
    image = await loaders.image_query(user_id_im=int(user_id)).first()
    return raw(image.image, content_type=image.image_mime_type)