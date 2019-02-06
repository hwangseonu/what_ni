from app import create_app
from config.db_config import LocalMongoDBConfig as MongoDBConfig
from config.app_config import DevConfig as Config

from constants import local_run as run

app = create_app(MongoDBConfig, Config)


if __name__ == '__main__':
    app.run(**run.RUN_SETTING)
