from flask import Flask
from flask_jwt_extended import JWTManager
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
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    jwt = JWTManager(app)
    return app
