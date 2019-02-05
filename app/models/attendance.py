from mongoengine import *
from datetime import datetime


class Attendance(Document):
    meta = {
        'collection': 'attendance'
    }

    attendance_date = DateTimeField(
        default=datetime.now,
        required=True
    )

    student = ReferenceField(
        document_type='StudentModel',
        primary_key=True
    )

    code = StringField(
        required=True
    )
