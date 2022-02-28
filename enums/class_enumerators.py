import enum
import os

class PathNames(str, enum.Enum):
    KEYS_FOLDER = 'keys'
    KEY = 'api-key-1645110930539.key'

class Currency(str, enum.Enum):
    EURO = 'EUR'
    USDT = 'USDT'

class Jinja(str, enum.Enum):
    TEMPLATE_FOLDER = 'templates'

class MongoDatabase(str, enum.Enum):
    DB_ADMIN = os.getenv('KRAKEN_DB_ADMIN')
    DB_PASSWORD = os.getenv('KRAKEN_DB_PASSWORD')
    DB_NAME = 'krakendb'
    DB_COLLECTION = 'dashboard_users'

class Host(str, enum.Enum):
    PUBLIC_ADDRESS = '3.65.98.218'
    PRIVATE_ADDRESS = '172.31.25.135'
    LOCALHOST = '127.0.0.1'
    USER = 'ubuntu'
    KEY_FOLDER = 'keys'
    KEY_FILE = 'mongo_kraken.pem'

class Ports(enum.IntEnum):
    SSH_TUNNEL_PORT = 22
    DB_PORT = 27017