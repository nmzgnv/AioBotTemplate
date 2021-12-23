import asyncio
import multiprocessing

from bot.main import init_bot
from config import DATABASE_URL
from demon.main import init_demon
from models.config import db
from models.user import User


async def main():
    await db.set_bind(DATABASE_URL)
    await db.gino.drop_all()
    await db.gino.create_all()
    # TODO assert tables exist

    # WARNING each process should connect to database
    task_1 = multiprocessing.Process(target=init_demon)
    task_2 = multiprocessing.Process(target=init_bot)

    task_2.start()
    task_1.start()

    while 1:
        print('User list got\n')
        all_users = await db.all(User.query)
        # for user in all_users:
        #     print(user)
        await asyncio.sleep(3)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
