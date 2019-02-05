from flask import Flask, Blueprint
from flask_restful import Api


def register_views(flask_app: Flask):
    handle_exception_func = flask_app.handle_exception
    handle_user_exception_func = flask_app.handle_user_exception

    api_blueprint = Blueprint('api_v1', __name__, url_prefix='/api')
    api = Api(api_blueprint)

    from app.views.student.account import StudentAccount
    api.add_resource(StudentAccount, '/student')
    from app.views.student.auth import StudentAuth, StudentRefresh
    api.add_resource(StudentAuth, '/student/auth')
    api.add_resource(StudentRefresh, '/student/auth/refresh')
    from app.views.student.attendance import StudentAttendance
    api.add_resource(StudentAttendance, '/attendance/<code>')

    from app.views.admin.account import AdminAccount
    api.add_resource(AdminAccount, '/admin')
    from app.views.admin.auth import AdminAuth, AdminRefresh
    api.add_resource(AdminAuth, '/admin/auth')
    api.add_resource(AdminRefresh, '/admin/auth/refresh')
    from app.views.admin.attendance import Code
    api.add_resource(Code, '/admin/code')

    flask_app.register_blueprint(api_blueprint)
    flask_app.handle_exception = handle_exception_func
    flask_app.handle_user_exception = handle_user_exception_func
