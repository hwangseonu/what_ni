from flask import Flask


def register_views(flask_app: Flask):
    from app.views import route
    route(flask_app)


def create_app():
    flask_app = Flask(__name__)
    register_views(flask_app)
    return flask_app
