"""
Init module
"""
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from .db import db
from .routes import main


def create_app():
    """
    Init application with:
    Flask
    CORS
    Swagger
    """
    app = Flask(__name__)
    Swagger(app)
    CORS(app)

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "sqlite:////tmp/pdf-app"  # Database configuration URI
    db.init_app(app)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
