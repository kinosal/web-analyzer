from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from app.config import ProductionConfig
from werkzeug.exceptions import HTTPException


db = SQLAlchemy()


def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    CORS(app, resources={r'/api/*': {'origins': '*'}})

    from app.api import require_key
    from app.api.v1 import api as api_v1

    app.register_blueprint(api_v1, url_prefix='/v1')

    @app.errorhandler(HTTPException)
    def handle_exception(error):
        """
        Return JSON instead of HTML for HTTP errors
        """
        response = {
            "code": error.code,
            "name": error.name,
            "description": error.description,
        }
        return jsonify(response)

    @app.route('/', methods=['GET'])
    def root():
        """
        Render index page
        """
        return render_template('index.html')

    @app.route('/ping', methods=['GET', 'POST'])
    @cross_origin()
    def ping() -> str:
        """
        Return string to show the server is alive
        """
        return 'Server is here'

    @app.route('/protected', methods=['GET'])
    @cross_origin()
    @require_key
    def protect() -> str:
        """
        Return string after successful authorization
        """
        return 'Valid key provided'

    return app
