"""
Registration of api on app
"""

from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import from module after Blueprint creation to avoid circularity
from app.api import user, errors  # NoQA
