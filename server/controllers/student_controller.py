from flask import Blueprint, request, Response, jsonify
from server.models.student_model import StudentModel

blueprint = Blueprint('student', 'student', url_prefix='/student')


@blueprint.route('/info', methods=['POST'])
def info():
    uuid = request.json['uuid']
    student = StudentModel.objects(uuid=uuid).first()
    return (jsonify({
        'student_id': student.student_id,
        'name': student.name,
        'birth': student.birth,
        'uuid': student.uuid,
        'profile_image': student.profile_image
    }), 200) if student else Response('', 404)
