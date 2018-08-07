from mongoengine import *


class AdminModel(Document):
    meta = {
        'collection': 'account_admin'
    }
    name = StringField(required=True)
    uid = StringField(required=True)
    pw = StringField(required=True)
    class_num = StringField(required=True)


