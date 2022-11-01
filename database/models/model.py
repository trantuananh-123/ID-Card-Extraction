from datetime import datetime
from email.policy import default
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.sql import functions as func, expression as exp
from database.models.not_null_column import NotNullColumn
from database.sql_alchemy_init import db


class Model(db.Model):
    id = Column(Integer, primary_key=True)
    name = NotNullColumn(String(100))
    url = NotNullColumn(String(1000))
    accurancy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    create_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
    status = NotNullColumn(Boolean)

    def __init__(self, name, url, status, accurancy=None, precision=None, recall=None, f1_score=None):
        self.name = name
        self.url = url
        self.status = status
        self.accurancy = accurancy
        self.precision = precision
        self.recall = recall
        self.f1_score = f1_score

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "accurancy": self.accurancy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "create_date": self.format_date(self.create_date),
            "update_date": self.format_date(self.update_date),
            "status": self.status
        }

    def format_date(self, date):
        if date != None:
            return date.strftime('%d/%m/%Y')
        return None
