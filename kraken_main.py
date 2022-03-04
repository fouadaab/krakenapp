from collections import defaultdict
from enums import class_enumerators
from core.config import settings
from db.db_client import MongoDB
from apis.base import api_router
from webapps.base import api_router as web_app_router
#from app import create_app, app_conf
from krakenapi.api_client import API
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import utils
import uvicorn
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

# Fill sum spent in EUR to hash table
for val in trades_eur.values():
    spent[class_enumerators.Currency.EURO] += str2float(val['cost'])


# @app.get("/spent/{currency}")
# def read_item(currency: str):
#     return {"sum spent in": currency, "total": spent[currency]}

def include_router(app):
    app.include_router(api_router)
    app.include_router(web_app_router)

def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    return app

app = start_application()


if __name__ == "__main__":    
    uvicorn.run("kraken_main:app", host='127.0.0.1', port=8000, reload=True)

    # server = create_app()
    # server.run(host=app_conf.config["host"], port=app_conf.config["port"])