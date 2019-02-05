from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity

from app.models.token import AccessTokenModel, RefreshTokenModel
from app.decorators.json_validator import json_validate
from app.models.account import StudentModel


class Auth(Resource):
    @json_validate({
        'type': 'object',
        'required': ['username', 'password'],
        'properties': {
            'username': {'type': 'string', 'minLength': 4},
            'password': {'type': 'string', 'minLength': 8}
        }
    })
    def post(self):
        payload = request.json

        account = StudentModel.objects(username=payload['username']).first()

        if not account:
            return {}, 404
        if account.password != payload['password']:
            return {}, 401

        return {'access': AccessTokenModel.create_access_token(account),
                'refresh': RefreshTokenModel.create_refresh_token(account)}, 200


class Refresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        username = get_jwt_identity()
        student = StudentModel.objects(username=username).first()

        if not student:
            return {}, 404

        return {"access": AccessTokenModel.create_access_token(student)}, 200
