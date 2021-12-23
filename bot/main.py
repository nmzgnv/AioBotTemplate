import asyncio

from config import DATABASE_URL
from models.config import db
from models.user import User


async def bot_task():
    await db.set_bind(DATABASE_URL)
    while 1:
        usr = await User.create(nickname='usr_1')
        print('1: ', usr)
        await asyncio.sleep(2)


def init_bot():
    # TODO get event loop and run bot task
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot_task())
