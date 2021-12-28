from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN

from models import GinoStorage

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = GinoStorage()
dp = Dispatcher(bot, storage=storage)
