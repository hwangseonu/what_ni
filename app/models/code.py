from mongoengine import *

from uuid import uuid4


class Code(Document):
    meta = {
        'collection': 'class_code'
    }
    identity = UUIDField(unique=True, default=uuid4)
    admin = ReferenceField(document_type='AdminModel', required=True)
    class_name = StringField(primary_key=True)
    start = DateTimeField(required=True)
    end = DateTimeField(required=True)
