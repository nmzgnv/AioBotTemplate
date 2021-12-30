import os

DB_HOST = 'localhost'
DB_NAME = 'AsyncBot'
DB_USER = 'admin'
DB_PASSWORD = 'admin'
DATABASE_URL = os.getenv('DATABASE_URL', f'asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

ADMIN_USER = os.getenv('ADMIN_USER', None)
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', None)
ADMIN_AUTH_DISABLE = os.getenv('ADMIN_AUTH_DISABLE', '1')

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_TG_IDS = [492621220]
