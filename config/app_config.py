import os


class DevConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'whatni_backend_api_secret')
