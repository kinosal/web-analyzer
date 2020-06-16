import os


class Config:
    """
    Base configuration for Flask app with testing, debug and tracking set to false
    """

    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """
    Add production PostgreSQL database connection from environment variables to Config
    """

    user = os.environ.get('PROD_DB_USER')
    pw = os.environ.get('PROD_DB_PW')
    url = os.environ.get('PROD_DB_URL')
    name = os.environ.get('PROD_DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{pw}@{url}/{name}'


class DevelopmentConfig(Config):
    """
    Set debug to true and add development PostgreSQL database connection
    from environment variables to Config
    """

    DEBUG = True
    user = os.environ.get('DEV_DB_USER')
    pw = os.environ.get('DEV_DB_PW')
    url = os.environ.get('DEV_DB_URL')
    name = os.environ.get('DEV_DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{pw}@{url}/{name}'


class TestingConfig(Config):
    """
    Set testing and debug to true and add testing SQLite database connection to Config
    """

    TESTING = True
    DEBUG = True
    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(basedir, 'tests/test.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{path}'


def set_config():  # pragma: no cover
    """
    Return appropriate Config class based on Flask environment
    """
    if os.environ.get('FLASK_ENV') == 'development':
        return DevelopmentConfig
    return ProductionConfig
