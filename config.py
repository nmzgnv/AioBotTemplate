import os

DB_HOST = 'localhost'
DB_NAME = 'AsyncBot'
DB_USER = 'admin'
DB_PASSWORD = 'admin'
DATABASE_URL = f'asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = [492621220]
