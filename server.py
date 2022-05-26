from sanic import Sanic
from sanic.response import text
from database import loaders,db
from sanic.response import json


app = Sanic('myapp')

class Config:
    PG_CONNECTION: str = None

app.config.load(Config)
app.config.load_environment_vars()

app.config.DB_DSN = app.config.PG_CONNECTION
db.init_app(app)
app.ctx.db = db


@app.get("/")
async def hello_world(request):
    all_users = await loaders.users_query().all()
    #return json([str(user.__dict__) for user in all_users])
    return json([user.to_dict() for user in all_users])


@app.post("/foo")
async def foo_handler(request):
    return text("I said foo!")

