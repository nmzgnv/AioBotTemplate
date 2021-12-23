import asyncio
import multiprocessing
import os

from gino_admin import create_admin_app

from bot.main import init_bot
from config import DB_NAME, DB_USER, DB_PASSWORD, DATABASE_URL
from daemon.main import init_daemon
from models.chat import Chat
from models.config import db
from models.user import User


async def init_db():
    await db.set_bind(DATABASE_URL)
    await db.gino.create_all()
    await db.pop_bind().close()


def init_server():
    # TODO configure normally
    os.environ["SANIC_DB_HOST"] = os.getenv("DB_HOST", "localhost")
    os.environ["SANIC_DB_DATABASE"] = DB_NAME
    os.environ["SANIC_DB_USER"] = DB_USER
    os.environ["SANIC_DB_PASSWORD"] = DB_PASSWORD

    os.environ["SANIC_ADMIN_USER"] = "admin"
    os.environ["SANIC_ADMIN_PASSWORD"] = "admin"

    create_admin_app(
        host="127.0.0.1",
        port=os.getenv("PORT", 8000),
        db=db,
        db_models=[User, Chat],
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    # TODO asyncio run checkpoints

    # WARNING each process should connect to database
    task_1 = multiprocessing.Process(target=init_daemon)
    task_2 = multiprocessing.Process(target=init_bot)

    # task_2.start()
    # task_1.start()

    init_server()
