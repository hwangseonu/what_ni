from flask import request, g
from flask_restful import Resource

from mongoengine import Q, NotUniqueError

from app.models.token import AccessTokenModel, RefreshTokenModel
from app.models.account import AdminModel
from app.decorators.json_validator import json_validate
from app.decorators.auth_required import auth_required


class AdminAccount(Resource):
    @json_validate({
        'type': 'object',
        'required': ['username', 'password', 'name', 'adminId'],
        'properties': {
            'username': {'type': 'string', 'minLength': 4},
            'password': {'type': 'string', 'minLength': 8},
            'name': {'type': 'string', 'pattern': '^[가-힣]{2,5}$'},
            'adminId': {'type': 'string', 'pattern': '^\\d+$'}
        }
    })
    def post(self):
        payload = request.json

        if AdminModel.objects.filter(Q(username=payload['username']) or Q(admin_id=payload['adminId'])).first():
            return {}, 409
        else:
            try:
                account = AdminModel(username=payload['username'],
                                     password=payload['password'],
                                     name=payload['name'],
                                     admin_id=payload['adminId']).save()
                return {'access': AccessTokenModel.create_access_token(account),
                        'refresh': RefreshTokenModel.create_refresh_token(account)}, 201
            except NotUniqueError:
                return {}, 409

    @auth_required(AdminModel)
    def get(self):
        account = g.user
        return {
                   "username": account.username,
                   "name": account.name,
                   "adminId": account.admin_id
               }, 200
