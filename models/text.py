from models.config import db
from sqlalchemy import String, Column, Integer


class Text(db.Model):
    __tablename__ = 'texts'
    id = Column(db.String(), primary_key=True, unique=True)

    name = Column(String(length=80), nullable=False)
    value = Column(db.UnicodeText)
    language = Column(String(length=2), default='ru')

    def __init__(self, name, value="empty text", language='ru'):
        self.name = name
        self.value = value
        self.language = language
