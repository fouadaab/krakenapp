import enum

class PathNames(str, enum.Enum):
    KEYS_FOLDER = 'keys'
    KEY = 'api-key-1645110930539.key'

class Currency(str, enum.Enum):
    EURO = 'EUR'
    USDT = 'USDT'