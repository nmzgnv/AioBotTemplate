from aiogram import types
from bot.loader import dp


@dp.message_handler(state='*')
async def echo(message: types.Message, user):
    await message.answer(message.text)
