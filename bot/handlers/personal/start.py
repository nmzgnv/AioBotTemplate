from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.loader import dp
from bot.text_utils import _
from models import User


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    await User.create_or_update_from_message(message)
    await message.answer(_('start_text'))
