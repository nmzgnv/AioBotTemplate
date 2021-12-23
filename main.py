import asyncio

from config import DATABASE_URL
from models.config import db
from models.user import User


async def main():
    await db.set_bind(DATABASE_URL)
    # await db.gino.drop()
    await db.gino.create_all()

    # Create user and database record
    user = await User.create(nickname='test')

    # Create user then database record
    user = User(nickname='test')
    user.nickname += '_2'
    await user.create()

    # explicitly close db
    await db.pop_bind().close()


asyncio.get_event_loop().run_until_complete(main())
