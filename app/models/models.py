"""Define app models."""

from sqlalchemy.exc import IntegrityError

from typing import List, Dict
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
    content = db.Column(db.String)
    entities_response = db.Column(db.JSON)
    artists_response = db.Column(db.JSON)
    artist_name = db.Column(db.String)
    artist_source = db.Column(db.String)
    external_id = db.Column(db.String)
    popularity = db.Column(db.Integer)


def save_url(
    url: str,
    content: str,
    entities: List[Dict],
    artists: List[Dict],
    source: str,
) -> None:
    url_model = Url(url=url)
    try:
        db.session.add(url_model)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    url_model = Url.query.filter(Url.url == url).first()
    url_model.artist_name = artists[0]["name"] if artists else None
    url_model.artist_source = source
    url_model.external_id = artists[0]["external_id"] if artists else None
    url_model.popularity = artists[0]["popularity"] if artists else None
    url_model.content = content
    url_model.entities_response = entities
    url_model.artists_response = artists
    db.session.commit()
