import os

DB_NAME = 'AsyncBot'
DB_USER = 'admin'
DB_PASSWORD = 'admin'
DATABASE_URL = f'asyncpg://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}'

BOT_TOKEN = os.getenv('BOT_SECRET_TOKEN', '1288081852:AAHzkoKuk5JH-ep-8ZuTp8F5GUuSouf_haw')
ADMINS = [492621220]
