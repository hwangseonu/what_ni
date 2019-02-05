from app import create_app
from config.db_config import MongoDBConfig

app = create_app(MongoDBConfig)


if __name__ == '__main__':
    app.run(debug=True)
