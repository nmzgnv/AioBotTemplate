import datetime
from aiogram import types
from loguru import logger

from models.config import db
from sqlalchemy import String, Column, Integer, Boolean, DateTime


class User(db.Model):
    __tablename__ = 'users'

    pk = Column(Integer(), primary_key=True)

    telegram_id = Column(String())
    username = Column(String(length=33), default='-')

    registration_date = Column(DateTime(), default=datetime.datetime.now())
    referer_id = Column(String(40), nullable=True)
    is_banned = Column(Boolean(), default=False)

    state = Column(String(50), default=None, nullable=True)
    state_data = Column(String(1000), default=None, nullable=True)

    def __str__(self):
        return f'{self.username} - {self.telegram_id}'

    @classmethod
    async def get(cls, telegram_id: str):
        return await User.query.where(User.telegram_id == telegram_id).gino.first()

    @classmethod
    async def create_or_update_from_message(cls, message: types.Message):
        str_tg_id = str(message.from_user.id)
        username = message.from_user.username

        saved_user = await User.query.where(User.telegram_id == str_tg_id).gino.first()
        if saved_user:
            if saved_user.username != username:
                logger.info(f"User {str_tg_id} changed username @{saved_user.username} to @{username}")
                await saved_user.update(username=username).apply()
            return saved_user

        referer_id = None
        command_args = message.get_args()
        if command_args:
            referer = await User.query.where(User.telegram_id == command_args.strip()).gino.first()
            if referer:
                referer_id = referer.telegram_id

        user = await User.create(telegram_id=str_tg_id, username=username, referer_id=referer_id)
        logger.info(f"User {str_tg_id} (@{username}) registered with referer: {referer_id}")

        return user
