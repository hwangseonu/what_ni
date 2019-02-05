from functools import wraps

from flask import abort, request
from jsonschema import ValidationError, validate


def json_validate(schema: dict):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.is_json:
                try:
                    validate(request.json, schema)
                except ValidationError:
                    abort(400)
            else:
                abort(406)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
