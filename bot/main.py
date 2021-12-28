import asyncio

from aiogram import executor
from loguru import logger

from bot.handlers import dp
from bot.text_utils import fill_db_texts_if_need, cached_texts, set_cached_texts_from_db
from bot.utils.notify_admins import on_startup_notify
from bot.utils.set_bot_commands import set_default_commands
from config import DATABASE_URL
from models import db


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    await db.set_bind(DATABASE_URL)


async def on_shutdown(dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await db.pop_bind().close()


def init_bot():
    loop = asyncio.get_event_loop()
    was_filled = loop.run_until_complete(fill_db_texts_if_need(cached_texts=cached_texts))
    if not was_filled:
        loop.run_until_complete(set_cached_texts_from_db())

    logger.info("Bot has been initialized")
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    init_bot()
