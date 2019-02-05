from flask import Flask, Blueprint
from flask_restful import Api


def register_views(flask_app: Flask):
    handle_exception_func = flask_app.handle_exception
    handle_user_exception_func = flask_app.handle_user_exception

    api_blueprint = Blueprint('api_v1', __name__, url_prefix='/api')
    api = Api(api_blueprint)

    from app.views.student.account import Account
    api.add_resource(Account, '/student')
    from app.views.student.auth import Auth, Refresh
    api.add_resource(Auth, '/student/auth')
    api.add_resource(Refresh, '/student/auth/refresh')
    from app.views.student.attendance import StudentAttendance
    api.add_resource(StudentAttendance, '/attendance/<code>')

    flask_app.register_blueprint(api_blueprint)
    flask_app.handle_exception = handle_exception_func
    flask_app.handle_user_exception = handle_user_exception_func
