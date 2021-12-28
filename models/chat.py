from models.config import db
from sqlalchemy import String, Column, Integer, BigInteger


class Chat(db.Model):
    __tablename__ = 'chats'

    id = Column(Integer(), primary_key=True, unique=True)

    telegram_id = Column(String(41))
    name = Column(String)
