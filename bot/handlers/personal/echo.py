from aiogram import types
from bot.loader import dp


@dp.message_handler(state='*')
async def bot_start(message: types.Message):
    await message.answer(message.text)
