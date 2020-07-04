import os
from flask import request
from functools import wraps


def require_auth(func):
    """
    Create decorator for authorization with Origin or API key
    """

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if 'Origin' in request.headers:
            secure_origins = os.environ.get('SECURE_ORIGINS').split(',')
            if request.headers['Origin'] in secure_origins:
                return func(*args, **kwargs)
        if 'API_KEY' not in request.headers:
            return 'Credentials missing', 401
        elif request.headers['API_KEY'] != os.environ.get('API_KEY'):
            return 'Credentials not valid', 401
        return func(*args, **kwargs)

    return func_wrapper
