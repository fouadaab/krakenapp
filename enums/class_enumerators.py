import enum
import os

class PathNames(str, enum.Enum):
    KEYS_FOLDER = 'keys'
    KEY = 'api-key-1645110930539.key'
    VENV = 'kraken_virtualenv'

class Currency(str, enum.Enum):
    EURO = 'EUR'
    USDT = 'USDT'

class Jinja(str, enum.Enum):
    TEMPLATE_FOLDER = 'templates'