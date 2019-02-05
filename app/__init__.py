from flask import Flask
from flask_jwt_extended import JWTManager
from mongoengine import connect
from app.views import register_views


def create_app(*config_cls):
    flask_app = Flask(__name__)
    register_views(flask_app)

    for config in config_cls:
        flask_app.config.from_object(config)

    connect(**flask_app.config['MONGODB_SETTINGS'])

    JWTManager().init_app(flask_app)

    return flask_app
