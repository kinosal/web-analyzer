"""
Api endpoints using a first (user) model
"""

from flask import jsonify
from app.api import api_bp, require_key
from app.models.models import User


@api_bp.route('/users', methods=['GET'])
@require_key
def get_users() -> str:
    """
    Retrieve all entries from DB and return count
    """
    return f'{User.query.count()} entries in DB'


@api_bp.route('/users/<int:id>', methods=['GET'])
@require_key
def get_user(id: int) -> object:
    """
    Return all properties for a single entry
    Args: id
    Returns: JSON with all properties
    """
    return jsonify(User.query.get_or_404(id).to_dict())
