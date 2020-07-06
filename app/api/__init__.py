"""Initialize API and provide decorators."""

from os import environ
from functools import wraps
from flask import request


def require_auth(func):
    """Create decorator for authorization with Origin or API key."""

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if "Origin" in request.headers:
            secure_origins = environ.get("SECURE_ORIGINS").split(",")
            if request.headers["Origin"] in secure_origins:
                return func(*args, **kwargs)
        if "API_KEY" not in request.headers:
            return "Credentials missing", 401
        if request.headers["API_KEY"] != environ.get("API_KEY"):
            return "Credentials not valid", 401
        return func(*args, **kwargs)

    return func_wrapper
