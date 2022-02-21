from collections import defaultdict
from enums import class_enumerators
from api import API
from fastapi import FastAPI
from typing import Optional
import utils
import pprint

spent = defaultdict(float)
def str2float(val: str) -> float:
    return float(val)

# API key and secret location
key_loc = utils.PathConstructor(class_enumerators.PathNames.KEYS_FOLDER.value, class_enumerators.PathNames.KEY.value)._str_path()

# Initialize API client
api_object = API()

# Read Kraken API key and secret stored in local file
api_object.load_key(key_loc)

# prepare request
req_data = {'trades': 'true'}

# query servers
trades_history = api_object.query_private('TradesHistory', req_data)

# process queried data
trades = trades_history['result']['trades']
trades_eur = {
    key:val for key,val in trades.items()
    if class_enumerators.Currency.EURO in val['pair']
    and class_enumerators.Currency.USDT not in val['pair']
}
# pprint.pprint(resp_eur)

# Fill sum spent in EUR to hash table
for val in trades_eur.values():
    spent[class_enumerators.Currency.EURO] += str2float(val['cost'])

app = FastAPI()

@app.get("/")
def read_root():
    return {"Application": "Kraken's Custom Wallet Dashboard"}

@app.get("/spent/{currency}")
def read_item(currency: str):
    return {"sum spent in": currency, "total": spent[currency]}