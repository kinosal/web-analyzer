"""
Define app models
"""

from typing import Dict
from app import db


class BaseModel(db.Model):
    """
    Base model with created_at and updated_at columns as well as
    a method to return all model properties as dict
    """
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self: object) -> Dict:
        data = {}
        columns = self.__table__.columns.keys()
        for key in columns:
            data[key] = getattr(self, key)
        return data


class User(BaseModel):
    """
    Representation of an initial (user) model
    """
    id = db.Column(db.Integer, primary_key=True)
