from app import create_app
from config.db_config import MongoDBConfig
from config.app_config import DevConfig

app = create_app(MongoDBConfig, DevConfig)


if __name__ == '__main__':
    app.run(debug=True)
