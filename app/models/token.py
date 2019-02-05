from uuid import uuid4

from flask_jwt_extended import create_access_token, create_refresh_token
from mongoengine import *

from app.models.account import AccountBase


class TokenBase(Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    class Key(EmbeddedDocument):
        owner = ReferenceField(
            document_type=AccountBase,
            required=True
        )

    key = EmbeddedDocumentField(
        document_type=Key,
        primary_key=True
    )

    identity = UUIDField(
        unique=True,
        default=uuid4
    )

    @classmethod
    def _create_token(cls, account):
        key = cls.Key(owner=account)
        cls.objects(key=key).delete()

        return cls(
            key=key
        ).save().identity


class AccessTokenModel(TokenBase):
    meta = {
        'collection': 'access_token'
    }

    @classmethod
    def create_access_token(cls, account):
        return create_access_token(
            str(cls._create_token(account))
        )


class RefreshTokenModel(TokenBase):
    meta = {
        'collection': 'refresh_token'
    }

    @classmethod
    def create_refresh_token(cls, account):
        return create_refresh_token(
            str(cls._create_token(account))
        )
