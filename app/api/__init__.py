import os
from flask import request
from functools import wraps


def require_key(func):
    """
    Create decorator for API key authorization
    """
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if 'API_KEY' not in request.headers:
            return 'Credentials missing', 401
        elif request.headers['API_KEY'] != os.environ.get('API_KEY'):
            return 'Credentials not valid', 401
        else:
            return func(*args, **kwargs)
    return func_wrapper
