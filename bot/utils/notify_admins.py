from aiogram import Dispatcher
from loguru import logger

from config import ADMIN_TG_IDS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMIN_TG_IDS:
        try:
            await dp.bot.send_message(admin, "Bot was started")

        except Exception as e:
            logger.error(f"Notify admin ({admin}) error: {e}")
