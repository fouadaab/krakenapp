from collections import defaultdict
from enums import class_enumerators
from core.config import settings
from apis.base import api_router
from webapps.base import api_router as web_app_router
from krakenapi.api_client import API as kraken_api
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import utils
import uvicorn
from pathlib import Path
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc, html
from app.dashapp.layout import layout
from app.dashapp.callbacks import register_callbacks
from starlette.middleware.wsgi import WSGIMiddleware

root_path = Path('.')

spent = defaultdict(float)
def str2float(val: str) -> float:
    return float(val)

# API key and secret location
key_loc = utils.PathConstructor(class_enumerators.PathNames.KEYS_FOLDER.value, class_enumerators.PathNames.KEY.value)._str_path()

# Initialize API client
krakenapi_client = kraken_api()

# Read Kraken API key and secret stored in local file
krakenapi_client.load_key(key_loc)

# prepare request
req_data = {'trades': 'true'}

# query servers
trades_history = krakenapi_client.query_private('TradesHistory', req_data)

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


def include_router(app):
    app.include_router(api_router)
    app.include_router(web_app_router)
    
def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp = dash.Dash(__name__,
                         requests_pathname_prefix='/dash/',
                         assets_folder= root_path / 'dashapp/assets',
                         meta_tags=[meta_viewport],
                         external_stylesheets=[dbc.themes.CERULEAN],
			 prevent_initial_callbacks=False,
			)

    dashapp.title = 'Dashapp'    
    dashapp.layout = layout
    register_callbacks(dashapp)
    
    app.mount("/dash", WSGIMiddleware(dashapp.server))

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    return app

app = start_application()

@app.get("/spent/{currency}")
def read_item(currency: str):
    return {"sum spent in": currency, "total": spent[currency]}


if __name__ == "__main__":
    uvicorn.run("kraken_main:app", host='127.0.0.1', port=8000, reload=True)

    # server = create_app()
    # server.run(host=app_conf.config["host"], port=app_conf.config["port"])