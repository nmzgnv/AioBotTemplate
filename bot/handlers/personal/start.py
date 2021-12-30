from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.loader import dp
from bot.text_utils import _


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    await message.answer(_('start_text'))
