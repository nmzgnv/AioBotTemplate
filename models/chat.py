from models.config import db
from sqlalchemy import String, Column, Integer


class Chat(db.Model):
    __tablename__ = 'chats'

    id = Column(Integer(), primary_key=True)

    telegram_id = Column(Integer())
    name = Column(String)
