from app import create_app
from config.db_config import LocalMongoDBConfig
from config.app_config import ProductionConfig

from constants import heroku_run as run

app = create_app(LocalMongoDBConfig, ProductionConfig)


if __name__ == '__main__':
    app.run(**run.RUN_SETTING)
