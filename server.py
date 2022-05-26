from sanic import Sanic

from blueprints import api
from database import db


app = Sanic('myapp')

class Config:
    PG_CONNECTION: str = None

app.config.load(Config)
app.config.load_environment_vars()

app.config.DB_DSN = app.config.PG_CONNECTION
db.init_app(app)
app.ctx.db = db

app.blueprint(api.blueprint)