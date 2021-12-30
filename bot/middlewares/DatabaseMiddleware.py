from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from models import User


class DatabaseMiddleware(BaseMiddleware):
    """
    Middleware to pass db models to handlers
    """

    async def on_pre_process_message(self, message: types.Message, data: dict):
        telegram_id = message.from_user.id
        user = await User.query.where(User.telegram_id == str(telegram_id)).gino.first()
        if not user:
            await User.create_or_update_from_message(message)
        elif user.is_banned:
            raise CancelHandler()

        data['user'] = user
