from mongoengine import *


class AttendanceModel(Document):
    meta = {
        'collection': 'attendance'
    }
    class_num = StringField(required=True)
    date = StringField(required=True)
    status = MapField(IntField(), required=True)


def get_attendance_by_class_and_date(cls, date):
    return AttendanceModel.objects(class_num=cls, date=date).first()
