from flask import Blueprint, request, Response, jsonify
from server.models.student_model import get_student_by_uuid
from server.models.attendance_model import get_attendance_by_class_and_date, AttendanceModel
from datetime import datetime

blueprint = Blueprint('attendance', 'attendance', url_prefix='/attendance')


@blueprint.route('/status/', methods=['POST'])
def status(uuid):
    uuid = request.json['uuid']
    student_id = get_student_by_uuid(uuid).student_id
    class_num = student_id[:3]
    num = student_id[3:]
    attendance = get_attendance_by_class_and_date(class_num)
    stat = attendance.status[num]
    return Response(str(stat), 200) if status else Response('', 404)


@blueprint.route('/check', methods=['POST'])
def check():
    uuid = request.json['uuid']
    status = request.json['status']
    student = get_student_by_uuid(uuid)

    if student:
        student_id = student.student_id
    else:
        return Response('Not Found UUID', 404)

    class_num = student_id[:3]
    num = student_id[3:]
    attendance = get_attendance_by_class_and_date(class_num, datetime.now().strftime('%Y.%m.%d'))

    if attendance:
        table = attendance.status
        table[num] = status
        attendance.update(set__status=table)
    else:
        AttendanceModel(class_num=class_num, date=datetime.now().strftime('%Y.%m.%d'), status={
            num: status
        }).save()
    return Response('', 201)
