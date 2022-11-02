from datetime import datetime
from email.policy import default
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import functions as func, expression as exp
from database.models.not_null_column import NotNullColumn
from database.sql_alchemy_init import db


class Label(db.Model):
    id = Column(Integer, primary_key=True)
    name = NotNullColumn(String(100), unique=True)
    create_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
    status = NotNullColumn(Boolean)

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "create_date": self.format_date(self.create_date),
            "update_date": self.format_date(self.update_date),
            "status": self.status
        }

    def format_date(self, date):
        if date != None:
            return date.strftime('%d/%m/%Y')
        return None
