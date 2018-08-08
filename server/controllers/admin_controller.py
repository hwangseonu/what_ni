import random
from flask import Blueprint, request, Response, jsonify
from flask_jwt_extended import create_access_token
from server.models.admin_model import AdminModel
from server.models.attendance_model import AttendanceModel
from server.models.student_model import StudentModel
from datetime import datetime

blueprint = Blueprint('admin', 'admin', url_prefix='/admin')
logined = dict()


@blueprint.route('/login', methods=['POST'])
def login():
    json = request.json
    id = json['id']
    pw = json['pw']
    admin = AdminModel.objects(uid=id, pw=pw).first()

    if not admin:
        return Response('', 404)

    token = create_access_token(identity=id)
    logined[token] = admin
    return jsonify({
        'access_token': token
    }), 200


@blueprint.route('/info', methods=['POST'])
def info():
    token = request.json['jwt']
    admin = logined[token]
    if not admin:
        return Response('', 404)
    return (jsonify({
        'name': admin.name,
        'id': admin.uid,
        'class_num': admin.class_num
    }), 200)


@blueprint.route('/table', methods=['POST'])
def table():
    token = request.json['jwt']
    admin = logined[token]
    class_num = admin.class_num
    date = datetime.now().strftime("%Y.%m.%d")
    att = AttendanceModel.objects(class_num=class_num, date=date)

    if not att:
        return Response('', 404)

    table = dict()
    att = att[0]
    for i in range(5):
        student = StudentModel.objects(uuid=str(12345 + i)).first()
        key = student.student_id + ' ' + student.name
        table[key] = [1, 1, att.status[student.student_id[3:]]]
        return jsonify(table), 200


@blueprint.route('/setstatus', methods=['POST'])
def setstatus():
    json = request.json
    token = json['jwt']
    admin = logined[token]

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


@blueprint.route('/count', methods=['POST'])
def count():
    admin = logined[request.json['jwt']]
    class_num = admin.class_num
    date = datetime.now().strftime("%Y.%m.%d")
    att = AttendanceModel.objects(date=date)
    if not att:
        att = AttendanceModel(class_num=class_num, date=date).save()
        return jsonify(attend=0, absent=len(att[0].status))
    else:
        att = att[0]
        status = att.status
        attend, absent = 0, 0

        for k, i in status.items():
            if i == 0:
                attend += 1
            else:
                absent += 1
        return jsonify(attend=attend, absent=absent), 200


@blueprint.route('/makecode', methods=['GET'])
def makecode():
    global now_code
    now_code = ''.join([chr(97 + i) for i in [random.randrange(0, 25) for i in range(10)]])
    return Response(now_code, 201)


@blueprint.route('/getcode', methods=['GET'])
def getcode():
    global now_code
    return Response(now_code, 200)


def get_now_code():
    global now_code
    return now_code
