from app import create_app
from config.db_config import LocalMongoDBConfig
from config.app_config import DevConfig

from constants import local_run

app = create_app(LocalMongoDBConfig, DevConfig)


if __name__ == '__main__':
    app.run(**local_run.RUN_SETTING)
