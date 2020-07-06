"""Define app models."""

from typing import Dict
from app import db


class BaseModel(db.Model):
    """Base model with default columns and method to return model properties as dict."""

    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self) -> Dict:
        """Create model columns dict.

        Args: self (model)
        Returns: property dict
        """
        data = {}
        columns = self.__table__.columns.keys()
        for key in columns:
            data[key] = getattr(self, key)
        return data


class User(BaseModel):
    """Representation of an initial (user) model."""

    id = db.Column(db.Integer, primary_key=True)
