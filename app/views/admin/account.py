from flask import request, g
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token

from mongoengine import Q

from app.models.account import AdminModel
from app.decorators.json_validator import json_validate
from app.decorators.auth_required import auth_required


class AdminAccount(Resource):
    @json_validate({
        'type': 'object',
        'required': ['username', 'password', 'name', 'studentId', 'birth', 'profileImage'],
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
            AdminModel(username=payload['username'],
                       password=payload['password'],
                       name=payload['name'],
                       admin_id=payload['adminId'])
            return {'access': create_access_token(payload['username']),
                    'refresh': create_refresh_token(payload['username'])}, 201

    @auth_required("admin")
    def get(self):
        account = g.user
        return {
                   "username": account.username,
                   "name": account.name,
                   "adminId": account.admin_id
               }, 200
