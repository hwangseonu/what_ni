from mongoengine import *
from server.models.student_model import StudentModel


class AttendanceModel(Document):
    meta = {
        'collection': 'attendance'
    }

    class_num = StringField(required=True)

    date = StringField(required=True)

    status = MapField(IntField(), required=True, default={s.student_id[3:]: 1 for s in StudentModel.objects()})

    reason = MapField(StringField(), required=False)
