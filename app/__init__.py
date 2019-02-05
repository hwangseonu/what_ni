from flask import Flask
from app.views import register_views

from mongoengine import connect


def create_app(*config_cls):
    flask_app = Flask(__name__)
    register_views(flask_app)

    for config in config_cls:
        flask_app.config.from_object(config)

    connect(flask_app.config['MONGODB_SETTINGS'])

    return flask_app
