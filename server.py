from sanic import Sanic
from sanic.response import text
#from . import config

app = Sanic('myapp')

app.config.DB_NAME = 'appdb'
app.config['DB_USER'] = 'appuser'

db_settings = {
    'DB_HOST': 'localhost',
    'DB_NAME': 'appdb',
    'DB_USER': 'appuser'
}

app.config.update(db_settings)
@app.get("/")
async def hello_world(request):
    return text("Hello, world.")


@app.get("/foo")
async def foo_handler(request):
    return text("I said foo!")
