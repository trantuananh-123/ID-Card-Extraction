from datetime import datetime
from email.policy import default
from re import M
from select import select
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import functions as func, expression as exp
from database.models.not_null_column import NotNullColumn
from database.sql_alchemy_init import db


class Example(db.Model):
    id = Column(Integer, primary_key=True)
    name = NotNullColumn(String(100), unique=True)
    url = NotNullColumn(String(100), unique=True)
    create_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
    status = NotNullColumn(Boolean)

    def __init__(self, name, url, status):
        self.name = name
        self.url = url
        self.status = status

    def serialize(sefl):
        return {
            "id": sefl.id,
            "name": sefl.name,
            "url": sefl.url,
            "create_date": sefl.create_date,
            "update_date": sefl.update_date,
            "status": sefl.status
        }

    def format_date(self, date):
        if date != None:
            return date.strftime('%d/%m/%Y')
        return None
