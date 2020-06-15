"""
Api error handling specifications
"""

from flask import jsonify
from werkzeug.exceptions import HTTPException
from app.api import api_bp


@api_bp.errorhandler(HTTPException)
def handle_exception(e: object) -> object:
    """
    Return JSON instead of HTML for HTTP errors
    """
    response = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }
    return jsonify(response)
