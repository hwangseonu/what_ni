from flask import Blueprint, request, Response, jsonify
from server.controllers.admin_controller import now_code
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
    code = request.json['code']

    if code != now_code:
        return Response('Not Match QR Code', 400)

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
        att = AttendanceModel(class_num=class_num, date=date).save()
        st = att.status
        st[num] = status
        att.update(set__stauts=st)
    return Response('', 201)


@blueprint.route('/reason', methods=['POST'])
def reason():
    json = request.json
    uuid = json['uuid']
    student = StudentModel.objects(uuid=uuid).first()
    if not student:
        return Response('Not Found UUID', 404)
    r = json['reason']
    date = datetime.now().strftime('%Y.%m.%d')
    class_num = student.student_id[:3]
    num = student.student_id[3:]
    att = AttendanceModel.objects(class_num=class_num)
    if not att:
        att = AttendanceModel(class_num=class_num, date=date, status={num: 1}, reason={num: r}).save()
    else:
        stat = att[0].status
        reas = att[0].reason
        stat[num] = 1
        reas[num] = r
        att[0].update(set__status=stat, set__reason=reas)
    return Response('', 201)
