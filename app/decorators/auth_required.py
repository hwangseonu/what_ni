from functools import wraps
from uuid import UUID

from flask import abort, g
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.token import AccessTokenModel


def auth_required(model):
    def decorator(fn):
        @wraps(fn)
        @jwt_required
        def wrapper(*args, **kwargs):
            try:
                token = AccessTokenModel.objects(identity=UUID(get_jwt_identity())).first()

                if token and isinstance(token.key.owner, model):
                    g.user = token.key.owner
                else:
                    abort(403)

                return fn(*args, **kwargs)
            except ValueError:
                abort(422)

        return wrapper

    return decorator
