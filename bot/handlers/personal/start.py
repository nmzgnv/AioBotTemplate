from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.loader import dp
from bot.text_utils import _
from models import User


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    # TODO register user
    await User.create(telegram_id=str(message.from_user.id), username=message.from_user.username)
    #
    await message.answer(_('start_text'))
