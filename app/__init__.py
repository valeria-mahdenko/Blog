import os

from flask import Flask, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from .config import config
from .exceptions import AppError

db = SQLAlchemy()
sess = Session()


def create_app(config_mode):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])
    app.secret_key = os.getenv('SECRET_KEY', 'test_key')

    sess.init_app(app)
    db.init_app(app)

    @app.errorhandler(AppError)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app
