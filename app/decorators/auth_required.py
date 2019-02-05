from functools import wraps

from flask import abort, g
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.account import StudentModel, AdminModel


def auth_required(account_type):
    def decorator(fn):
        @wraps(fn)
        @jwt_required
        def wrapper(*args, **kwargs):
            try:
                username = get_jwt_identity()
                if account_type == "student":
                    account = StudentModel.objects(username=username).first()
                    if not account:
                        abort(404)
                    g.user = account
                elif account_type == "admin":
                    account = AdminModel.objects(username=username)
                    if not account:
                        abort(404)
                    g.user = account
                else:
                    abort(401)
                return fn(*args, **kwargs)
            except ValueError:
                abort(422)
        return wrapper
    return decorator
