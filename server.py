from sanic import Sanic
from sanic.response import text
from database.models.models import db,User
import json
from database import loaders

app = Sanic('myapp')
'''
class Config:
    PG_CONNECTION: str = None

app.config.load(Config)
app.config.load_environment_vars()

app.config.DB_DSN = app.config.PG_CONNECTION
db.init_app(app)
app.ctx.db = db
'''

@app.get("/")
async def hello_world(request):
    all_users = await loaders.users_query().all()
    all_users = json([user.to_dict() for user in all_users])
    return all_users


@app.post("/foo")
async def foo_handler(request):
    return text("I said foo!")

