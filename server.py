from sanic import Blueprint, Sanic

from blueprints import users
import blueprints
from database import db


app = Sanic('myapp')

class Config:
    PG_CONNECTION: str = None

app.config.load(Config)
app.config.load_environment_vars()

app.config.DB_DSN = app.config.PG_CONNECTION
db.init_app(app)
app.ctx.db = db

#app.blueprint(users_bp.blueprint) #сделать группу
app.blueprint(Blueprint.group(
    blueprints.image.blueprint,
    blueprints.users.blueprint,
    #url_prefix=app.config.APP_URL_PREFIX
))