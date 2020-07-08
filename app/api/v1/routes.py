"""Endpoints for API v1."""

from flask import jsonify
from flask_restx import Api
from flask_restx import Resource

from app.api import require_auth
from app.api.v1 import api_v1
from app.models.models import User

api = Api(
    api_v1,
    version="1.0",
    title="My API",
    description="Serving data to the world",
)

users = api.namespace("users", description="user data")


@users.route("/")
class UserCount(Resource):
    @require_auth
    @api.doc(
        responses={200: "Success", 401: "Unauthorized"},
        params={"API_KEY": {"in": "header"}},
    )
    def get(self) -> str:
        """Show number of users in database."""
        return f"{User.query.count()} entries in DB"


@users.route("/<int:user_id>")
class UserObject(Resource):
    @require_auth
    @api.doc(
        responses={200: "Success", 401: "Unauthorized", 404: "Entry not found"},
        params={
            "user_id": "Specify the id of the user of interest",
            "API_KEY": {"in": "header"},
        },
    )
    def get(self, user_id: int) -> object:
        """Return all properties for a single entry.

        Args: id
        Returns: JSON with all properties
        """
        return jsonify(User.query.get_or_404(user_id).to_dict())
