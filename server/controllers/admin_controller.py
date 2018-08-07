import random
from flask import Blueprint, request, Response, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from server.models.admin_model import AdminModel
from server.models.attendance_model import AttendanceModel
from server.models.student_model import StudentModel
from datetime import datetime

blueprint = Blueprint('admin', 'admin', url_prefix='/admin')
now_code = ''.join([chr(97 + i) for i in [random.randrange(0, 25) for i in range(10)]])


@blueprint.route('/login', methods=['POST'])
def login():
    json = request.json
    id = json['id']
    pw = json['pw']
    admin = AdminModel.objects(uid=id, pw=pw).first()

    if not admin:
        return Response('', 404)

    return jsonify({
        'access_token': create_access_token(identity=id),
        'refresh_token': create_refresh_token(identity=id)
    }), 200


@blueprint.route('/info', methods=['GET'])
@jwt_required
def info():
    id = get_jwt_identity()
    admin = AdminModel.objects(uid=id).first()
    return (jsonify({
        'name': admin.name,
        'id': admin.uid,
        'pw': admin.pw,
        'class': admin.class_num
    }), 200)


@blueprint.route('/attendance', methods=['GET'])
@jwt_required
def attendance():
    id = get_jwt_identity()
    admin = AdminModel.objects(uid=id).first()
    class_num = admin.class_num
    date = datetime.now().strftime("%Y.%m.%d")
    att = AttendanceModel.objects(class_num=class_num, date=date)

    if not att:
        return Response('', 404)

    table = dict()
    att = att[0]
    for i in range(5):
        student = StudentModel.objects(uuid=str(12346 - i)).first()
        key = student.student_id + ' ' + student.name
        table[key] = [1, 1, att.status[student.student_id[3:]]]


@blueprint.route('/setstatus', methods=['POST'])
@jwt_required
def setstatus():
    json = request.json
    id = get_jwt_identity()
    admin = AdminModel.objects(uid=id).first()

    date = json['date']
    student_num = json['student_num']
    stats = json['status']
    class_num = admin.class_num
    att_table = AttendanceModel.objects(class_num=class_num, date=date)

    if not att_table:
        AttendanceModel(class_num=class_num, date=date, stats={
            student_num: stats
        })
    else:
        att_table = att_table[0]
        status = att_table.status
        stats[student_num] = stats
        att_table.update(set__status=status)

    return Response('', 201)


@blueprint.route('/makecode', methods=['GET'])
def makecode():
    global now_code
    now_code = ''.join([chr(97 + i) for i in [random.randrange(0, 25) for i in range(10)]])
    return Response(now_code, 201)


@blueprint.route('/getcode', methods=['GET'])
def getcode():
    return Response(now_code, 200)
