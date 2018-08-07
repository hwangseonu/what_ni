from flask import Blueprint, request, Response, jsonify
from server.models.student_model import StudentModel
from server.models.attendance_model import AttendanceModel
from datetime import datetime

blueprint = Blueprint('attendance', 'attendance', url_prefix='/attendance')


@blueprint.route('/status', methods=['POST'])
def status():
    uuid = request.json['uuid']
    date = datetime.now().strftime('%Y.%m.%d')
    student_id = StudentModel.objects(uuid=uuid).first().student_id
    class_num = student_id[:3]
    num = student_id[3:]
    attendance = AttendanceModel.objects(class_num=class_num, date=date).first()
    stat = attendance.status[num]
    return Response(str(stat), 200) if status else Response('', 404)


@blueprint.route('/check', methods=['POST'])
def check():
    uuid = request.json['uuid']
    status = request.json['status']
    student = StudentModel.objects(uuid=uuid).first()
    date = datetime.now().strftime('%Y.%m.%d')
    if student:
        student_id = student.student_id
    else:
        return Response('Not Found UUID', 404)

    class_num = student_id[:3]
    num = student_id[3:]
    attendance = AttendanceModel.objects(class_num=class_num, date=date).first()

    if attendance:
        table = attendance.status
        table[num] = status
        attendance.update(set__status=table)
    else:
        AttendanceModel(class_num=class_num, date=date, status={
            num: status
        }).save()
    return Response('', 201)
