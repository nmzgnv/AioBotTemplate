from aiogram import Bot, Dispatcher, types

# from bot.states.SQLAlchemyStorage import SQLAlchemyStorage
from config import BOT_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
# TODO write GINO storage
# storage = SQLAlchemyStorage()
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
