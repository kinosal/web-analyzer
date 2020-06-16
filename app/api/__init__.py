"""
Registration of api on app
"""

import os
from flask import Blueprint, request
from functools import wraps

api_bp = Blueprint('api', __name__)


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


# Import from module after Blueprint creation to avoid circularity
from app.api import user, errors  # NoQA
