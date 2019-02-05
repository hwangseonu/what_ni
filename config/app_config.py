import os


class DevConfig:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'whatni_backend_api_secret')
