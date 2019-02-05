from flask import request, g
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from mongoengine import Q

from app.models.account import StudentModel
from app.decorators.json_validator import json_validate
from app.decorators.auth_required import auth_required


class Account(Resource):
    @json_validate({
        'type': 'object',
        'required': ['username', 'password', 'name', 'studentId', 'birth', 'profileImage'],
        'properties': {
            'username': {'type': 'string', 'minLength': 4},
            'password': {'type': 'string', 'minLength': 8},
            'name': {'type': 'string', 'pattern': '^[가-힣]{2,5}$'},
            'studentId': {'type': 'string', 'pattern': '^\\d+$'},
            'birth': {'type': 'string', 'format': 'date-time'},
            'profileImage': {'type': 'string'}
        }
    })
    def post(self):
        payload = request.json

        if StudentModel.objects.filter(Q(username=payload['username']) or Q(student_id=payload['studentId'])).first():
            return {}, 409
        else:
            StudentModel(username=payload['username'],
                         password=payload['password'],
                         name=payload['name'],
                         student_id=payload['studentId'],
                         birth=payload['birth'],
                         profile_image=payload['profileImage']).save()
            return {'access': create_access_token(payload['username']),
                    'refresh': create_refresh_token(payload['username'])}, 201

    @auth_required("student")
    def get(self):
        account = g.user
        return {
            "username": account.username,
            "name": account.name,
            "studentId": account.student_id,
            "birth": account.birth,
            "profileImage": account.profile_image
        }, 200
