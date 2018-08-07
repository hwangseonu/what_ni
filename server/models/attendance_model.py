from mongoengine import *


class AttendanceModel(Document):
    meta = {
        'collection': 'attendance'
    }

    class_num = StringField(required=True)

    date = StringField(required=True)

    status = MapField(IntField(), required=True)
