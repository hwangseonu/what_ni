from datetime import datetime
from uuid import UUID

from flask import request, g
from flask_restful import Resource

from app.models.code import Code as CodeModel
from app.models.attendance import Attendance
from app.models.account import AdminModel
from app.decorators.json_validator import json_validate
from app.decorators.auth_required import auth_required


class Code(Resource):
    @json_validate({
        'type': 'object',
        'required': ['class_name', 'start', 'end'],
        'properties': {
            'class_name': {'type': 'string'},
            'start': {'type': 'string', 'format': 'date-time'},
            'end': {'type': 'string', 'format': 'date-time'},
        }
    })
    @auth_required(AdminModel)
    def post(self):
        payload = request.json

        code = CodeModel.objects(class_name=payload['class_name']).first()

        if code:
            code.delete()

        start = datetime.strptime(payload['start'], '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(payload['end'], '%Y-%m-%d %H:%M:%S')
        code = CodeModel(admin=g.user, class_name=payload['class_name'], start=start, end=end).save()

        return {
            'code': str(code.identity)
        }, 201


class AdminAttendance(Resource):
    @auth_required(AdminModel)
    def get(self, code):
        cls = CodeModel.objects(identity=UUID(code)).first()
        if cls.admin != g.user:
            return {}, 403

        return [{
            "attendanceDate": str(i.attendance_date),
            "student": {
                "username": i.student.username,
                "name": i.student.name,
                "studentId": i.student.student_id,
            }
        } for i in Attendance.objects(code=UUID(code)).all()], 200
