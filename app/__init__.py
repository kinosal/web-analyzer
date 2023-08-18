"""Flask app factory."""

from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException


db = SQLAlchemy()


def create_app(config_class: object):
    """Create Flask app.

    Args:
        config_class: configuation for Flask app
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from app.api import require_auth
    from app.api.v1 import api_v1

    app.register_blueprint(api_v1)

    @app.errorhandler(HTTPException)
    def handle_exception(error):
        """Return JSON instead of HTML for HTTP errors."""
        response = {
            "code": error.code,
            "name": error.name,
            "description": error.description,
        }
        return jsonify(response)

    @app.route("/ping", methods=["GET", "POST"])
    def ping() -> str:
        """Return string to show the server is alive."""
        return "Server is here"

    @app.route("/protected", methods=["GET", "POST"])
    @require_auth
    def protect() -> str:
        """Return string after successful authorization."""
        return "Valid key provided"

    return app
