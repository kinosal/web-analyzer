"""Define app models."""

from sqlalchemy.exc import IntegrityError

from typing import Dict
from app import db


class BaseModel(db.Model):
    """Base model with default columns and method to return model properties as dict."""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
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


class Url(BaseModel):
    url = db.Column(db.String, unique=True, nullable=False)
    artist_name = db.Column(db.String)
    artist_source = db.Column(db.String)
    external_id = db.Column(db.String)
    popularity = db.Column(db.Integer)


def save_url(url: str, source: str, artist: Dict) -> None:
    url_model = Url(
        url=url,
        artist_name=artist["name"],
        artist_source=source,
        external_id=artist["external_id"],
        popularity=artist["popularity"],
    )
    db.session.add(url_model)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        url_model = Url.query.filter(Url.url == url).first()
        url_model.artist_name = artist["name"]
        url_model.artist_source = source
        url_model.external_id = artist["external_id"]
        url_model.popularity = artist["popularity"]
        db.session.commit()
