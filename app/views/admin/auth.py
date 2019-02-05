from uuid import UUID

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity

from app.models.token import AccessTokenModel, RefreshTokenModel
from app.decorators.json_validator import json_validate
from app.models.account import AdminModel


class AdminAuth(Resource):
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

        account = AdminModel.objects(username=payload['username']).first()

        if not account:
            return {}, 404
        if account.password != payload['password']:
            return {}, 401

        return {'access': AccessTokenModel.create_access_token(account),
                'refresh': RefreshTokenModel.create_refresh_token(account)}, 200


class AdminRefresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        token = RefreshTokenModel.objects(identity=UUID(get_jwt_identity())).first()

        if not token:
            return {}, 422

        return {"access": AccessTokenModel.create_access_token(token.key.owner)}, 200
