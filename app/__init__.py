from flask import Flask
from app.views import register_views


def create_app():
    flask_app = Flask(__name__)
    register_views(flask_app)
    return flask_app
