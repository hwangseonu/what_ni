import os


class LocalMongoDBConfig:
    MONGODB_SETTINGS = {
        'db': 'what_ni',
        'host': 'localhost',
        'port': 27017
    }


class HerokuMongoDBConfig:
    MONGODB_SETTINGS = {
        'db': 'what_ni',
        'host': os.getenv('MONGODB_URI'),
        'port': 27017
    }
