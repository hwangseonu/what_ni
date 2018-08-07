from flask import Blueprint, request, Response, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from server.models.admin_model import AdminModel
from server.models.attendance_model import AttendanceModel
from datetime import datetime

blueprint = Blueprint('admin', 'admin', url_prefix='/admin')
blacklist = set()


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
        return Response('Not Found Data', 404)
    return jsonify({
        'class': class_num,
        'date': date,
        'table': att.status
    }), 200
