import asyncio

from config import DATABASE_URL
from models.config import db
from models.user import User


async def demon_task():
    await db.set_bind(DATABASE_URL)
    while 1:
        usr = await User.create(nickname='usr_2')
        print('2: ', usr)
        await asyncio.sleep(2)


def init_demon():
    # TODO get event loop and run demon task
    loop = asyncio.get_event_loop()
    loop.run_until_complete(demon_task())
