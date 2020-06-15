import os


def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def create_db_url(user, pw, url, db):
    return f"postgresql://{user}:{pw}@{url}/{db}"


POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_DB = get_env_variable("POSTGRES_DB")


class Config():
    SQLALCHEMY_DATABASE_URI = \
        create_db_url(POSTGRES_USER, POSTGRES_PW, POSTGRES_URL, POSTGRES_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
