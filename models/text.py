from models.config import db
from sqlalchemy import String, Column, Integer


class Text(db.Model):
    __tablename__ = 'texts'
    id = db.Column(db.Integer(), primary_key=True)

    name = Column(String(length=80), nullable=False)
    value = Column(db.UnicodeText)
    language = Column(String(length=2), default='ru')
