import os
from pathlib import Path
from enums import class_enumerators

from dotenv import load_dotenv

env_path = Path(os.getenv('WORKON_HOME')) / class_enumerators.PathNames.VENV
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Kraken Dashboard Application"
    PROJECT_VERSION: str = "1.0.0"

    DB_ADMIN = os.getenv('KRAKEN_DB_ADMIN')
    DB_PASSWORD = os.getenv('KRAKEN_DB_PASSWORD')
    DB_NAME = 'krakendb'
    DB_COLLECTION = 'dashboard_users'

    PUBLIC_ADDRESS = '3.65.98.218'
    PRIVATE_ADDRESS = '172.31.25.135'
    LOCALHOST = '127.0.0.1'
    USER = 'ubuntu'
    KEY_FOLDER = 'keys'
    KEY_FILE = 'mongo_kraken.pem'

    SSH_TUNNEL_PORT = 22
    DB_PORT = 27017

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins
    ALGORITHM = "HS256"


settings = Settings()