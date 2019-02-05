from flask import Flask, Blueprint
from flask_restful import Api


def register_views(flask_app: Flask):
    handle_exception_func = flask_app.handle_exception
    handle_user_exception_func = flask_app.handle_user_exception

    api_blueprint = Blueprint('api_v1', __name__, url_prefix='/api')
    api = Api(api_blueprint)

    from app.views.users.users import User
    api.add_resource(User, '/users')

    flask_app.register_blueprint(api_blueprint)
    flask_app.handle_exception = handle_exception_func
    flask_app.handle_user_exception = handle_user_exception_func
