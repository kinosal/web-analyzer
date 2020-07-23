"""Flask app configurations."""

from os import environ
from os import path


class Config:
    """Base configuration for Flask app."""

    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production config with PostgreSQL database connection."""

    user = environ.get("PROD_DB_USER")
    pw = environ.get("PROD_DB_PW")
    url = environ.get("PROD_DB_URL")
    name = environ.get("PROD_DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{pw}@{url}/{name}"


class DevelopmentConfig(Config):
    """Development config with PostgreSQL database connection."""

    DEBUG = True
    user = environ.get("DEV_DB_USER")
    pw = environ.get("DEV_DB_PW")
    url = environ.get("DEV_DB_URL")
    name = environ.get("DEV_DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{pw}@{url}/{name}"


class TestingConfig(Config):
    """Testing config with SQLite database connection."""

    TESTING = True
    DEBUG = True
    basedir = path.dirname(path.dirname(path.abspath(__file__)))
    db_path = path.join(basedir, "tests/test.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"


def set_config():  # pragma: no cover
    """Return appropriate Config class based on Flask environment."""
    if environ.get("FLASK_ENV") == "development":
        return DevelopmentConfig
    return ProductionConfig
