"""
Endpoints for API v1
"""

from flask import jsonify
from app.api import require_auth
from app.api.v1 import api
from app.models.models import User


@api.route('/users', methods=['GET'])
@require_auth
def get_users() -> str:
    """
    Retrieve all entries from DB and return count
    """
    return f'{User.query.count()} entries in DB'


@api.route('/users/<int:id>', methods=['GET'])
@require_auth
def get_user(id: int) -> object:
    """
    Return all properties for a single entry
    Args: id
    Returns: JSON with all properties
    """
    return jsonify(User.query.get_or_404(id).to_dict())
