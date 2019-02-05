from uuid import UUID

from flask import g
from flask_restful import Resource

from app.models.account import StudentModel
from app.models.code import Code as CodeModel
from app.models.attendance import Attendance
from app.decorators.auth_required import auth_required


class StudentAttendance(Resource):
    @auth_required(StudentModel)
    def post(self, code):
        account = g.user

        attendance = Attendance.objects(student=account, code=UUID(code)).first()
        cls = CodeModel.objects(identity=UUID(code)).first()

        if not cls:
            return {}, 404

        if attendance:
            attendance.delete()

        attendance = Attendance(student=account, code=UUID(code)).save()

        return {
                   "student": {
                       "username": account.username,
                       "name": account.name,
                       "studentId": account.student_id,
                       "birth": account.birth,
                       "profileImage": account.profile_image
                   },
                   "class": {
                       "className": cls.class_name,
                       "start": cls.start,
                       "end": cls.end
                   },
                   "code": attendance.code,
                   "attendanceDate": attendance.attendance_date
               }, 200

    @auth_required(StudentModel)
    def get(self, code):
        account = g.user

        attendance = Attendance.objects(student=account, code=UUID(code)).first()
        cls = CodeModel.objects(identity=UUID(code)).first()

        if not attendance or not cls:
            return {}, 404

        return {
                   "student": {
                       "username": account.username,
                       "name": account.name,
                       "studentId": account.student_id,
                       "birth": account.birth,
                       "profileImage": account.profile_image
                   },
                   "class": {
                       "className": cls.class_name,
                       "start": cls.start,
                       "end": cls.end
                   },
                   "code": attendance.code,
                   "attendance_date": attendance.attendance_date
               }, 200
