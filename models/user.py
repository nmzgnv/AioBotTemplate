import datetime
from typing import Optional

from models.config import db
from sqlalchemy import String, Column, Integer, Boolean, DateTime


class User(db.Model):
    __tablename__ = 'users'

    pk = Column(Integer(), primary_key=True)

    telegram_id = Column(String())
    username = Column(String(length=33), default='-')

    registration_date = Column(DateTime(), default=datetime.datetime.now())
    referer_id = Column(String(40))
    is_banned = Column(Boolean(), default=False)

    state = Column(String(50), default=None, nullable=True)
    state_data = Column(String(1000), default=None, nullable=True)

    def __str__(self):
        return f'{self.nickname} - {self.telegram_id}'

    @classmethod
    async def get(cls, telegram_id: str):
        return await User.query.where(User.telegram_id == telegram_id).gino.first()
