import asyncio
import multiprocessing
import os

from gino_admin import create_admin_app, add_admin_panel
from sanic import Sanic, response

from bot.main import init_bot
from config import DB_NAME, DB_USER, DB_PASSWORD, DATABASE_URL
from daemon.main import init_daemon
from models.chat import Chat
from models.config import db
from models.user import User

app = Sanic(name=__name__)


@app.route("/")
async def index(request):
    return response.redirect("/admin")


async def init_db():
    await db.set_bind(DATABASE_URL)
    await db.gino.create_all()
    await db.pop_bind().close()


def init_server() -> Sanic:
    # TODO configure normally
    app.config["DB_HOST"] = os.getenv("DB_HOST", "localhost")
    app.config["DB_DATABASE"] = DB_NAME
    app.config["DB_USER"] = DB_USER
    app.config["DB_PASSWORD"] = DB_PASSWORD

    app.config["ADMIN_USER"] = "admin"
    app.config["ADMIN_PASSWORD"] = "admin"

    add_admin_panel(
        name='Bot admin',
        app=app,
        db=db,
        db_models=[User, Chat],
    )
    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    # TODO asyncio run checkpoints
    # 1) Token exist
    # 2) Tables exist

    # WARNING each process should connect to database
    daemon = multiprocessing.Process(target=init_daemon)
    bot = multiprocessing.Process(target=init_bot)

    bot.start()
    daemon.start()

    app = init_server()
    app.run(host="127.0.0.1", port=os.getenv("PORT", 8000), debug=False, auto_reload=False)
