from flask import Flask
from mongoengine import connect
from server.controllers import init_controllers


def create_app():
    app = Flask('what_ni')
    app.config['MONGODB_SETTINGS'] = {
        'db': 'what_ni',
        'host': 'localhost',
        'port': 27017
    }
    connect(**app.config['MONGODB_SETTINGS'])
    init_controllers(app)
    return app
