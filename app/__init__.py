from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.config import Config


db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from app.api import api_bp, errors  # NoQA
    app.register_blueprint(api_bp)

    @app.route('/ping', methods=['GET', 'POST'])
    def ping():
        """
        Return string to show the server is alive
        """
        return 'Server is here'

    @app.route('/', methods=['GET'])
    def root():
        """
        Render index page
        """
        return render_template('index.html')

    return app
