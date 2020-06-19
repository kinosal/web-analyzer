from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from app.config import ProductionConfig


db = SQLAlchemy()


def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    CORS(app, resources={r'/api/*': {'origins': '*'}})

    from app.api import api_bp, require_key  # NoQA

    app.register_blueprint(api_bp, url_prefix='/api')

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
