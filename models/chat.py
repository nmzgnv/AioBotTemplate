from models.config import db
from sqlalchemy import String, Column, Integer


class Chat(db.Model):
    __tablename__ = 'chats'

    id = Column(db.String(), primary_key=True, unique=True)

    telegram_id = Column(Integer())
    name = Column(String)
