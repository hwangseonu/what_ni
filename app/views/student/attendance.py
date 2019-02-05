from flask import g
from flask_restful import Resource

from app.models.attendance import Attendance
from app.decorators.auth_required import auth_required


class StudentAttendance(Resource):
    @auth_required('student')
    def post(self, code):
        account = g.user
        attendance = Attendance.objects(student=account, code=code).first()

        if attendance:
            return {}, 409

        attendance = Attendance(student=account, code=code).save()

        return {
                   "student": {
                       "username": account.username,
                       "name": account.name,
                       "studentId": account.student_id,
                       "birth": account.birth,
                       "profileImage": account.profile_image
                   },
                   "code": attendance.code,
                   "attendance_date": attendance.attendance_date
               }, 200

    @auth_required
    def get(self, code):
        account = g.user
        attendance = Attendance.objects(student=account, code=code).first()

        if attendance:
            return {}, 404

        return {
                   "student": {
                       "username": account.username,
                       "name": account.name,
                       "studentId": account.student_id,
                       "birth": account.birth,
                       "profileImage": account.profile_image
                   },
                   "code": attendance.code,
                   "attendance_date": attendance.attendance_date
               }, 200
