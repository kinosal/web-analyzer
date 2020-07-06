"""Initialize API version by creating Blueprint and importing routes."""

from flask import Blueprint

api = Blueprint("api", __name__)

from app.api.v1 import routes  # NoQA
