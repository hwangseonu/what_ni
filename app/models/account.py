from mongoengine import *


class AccountBase(Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }
    username = StringField(primary_key=True)
    password = StringField(required=True)
    name = StringField(required=True)


class StudentModel(AccountBase):
    meta = {
        'collection': 'account_student'
    }
    student_id = StringField(unique=True, required=True)
    birth = StringField(required=True)
    profile_image = StringField(required=True)


class AdminModel(AccountBase):
    meta = {
        'collection': 'account_admin'
    }
    admin_id=StringField(unique=True, required=True)
