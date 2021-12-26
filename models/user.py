from models.config import db
from sqlalchemy import String, Column, Integer


class User(db.Model):
    __tablename__ = 'users'

    pk = Column(db.Integer(), primary_key=True)

    telegram_id = Column(Integer())
    nickname = Column(String(length=33), default='-')

    def __str__(self):
        return f'{self.nickname} - {self.telegram_id}'
