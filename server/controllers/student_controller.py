from flask import Blueprint, request, Response, jsonify
from server.models.student_model import get_student_by_uuid

blueprint = Blueprint('student', 'student', url_prefix='/student')


@blueprint.route('/info', methods=['POST'])
def info():
    uuid = request.json['uuid']
    student = get_student_by_uuid(uuid)
    return (jsonify({
        'student_id': student.student_id,
        'name': student.name,
        'birth': student.birth,
        'uuid': student.uuid
    }), 200) if student else Response('', 404)
