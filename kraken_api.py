from collections import defaultdict
from enums import class_enumerators
from db.db_client import MongoDB
#from app import create_app, app_conf
from api.api_client import API
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

app = FastAPI()
templates = Jinja2Templates(directory=class_enumerators.Jinja.TEMPLATE_FOLDER)
staticfiles = StaticFiles(directory="static")
app.mount("/static", staticfiles, name="static")

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("demo.html", {"request": request, "title": "Kraken App Demo", "body_content": "This is where we gather up to show our love and devotion to XRP"})

@app.get("/spent/{currency}")
def read_item(currency: str):
    return {"sum spent in": currency, "total": spent[currency]}

@app.get("/users/{username}")
def read_item(username: str):
    client = MongoDB()
    client.db_find(
        db_name=class_enumerators.MongoDatabase.DB_NAME.value,
        db_col=class_enumerators.MongoDatabase.DB_COLLECTION.value,
        db_admin=class_enumerators.MongoDatabase.DB_ADMIN.value,
        db_pass=class_enumerators.MongoDatabase.DB_PASSWORD.value,
    )

    for user in client.docs:
        if user['username'] == username:
            return user

    return {f"User '{username}'": "Not registered in our Database"}

if __name__ == "__main__":
    uvicorn.run("kraken_api:app", host='127.0.0.1', port=8000, reload=True)

    # server = create_app()
    # server.run(host=app_conf.config["host"], port=app_conf.config["port"])
    
    # client = MongoDB()
    # client.db_find(
    #     db_name=class_enumerators.MongoDatabase.DB_NAME.value,
    #     db_col=class_enumerators.MongoDatabase.DB_COLLECTION.value,
    #     db_admin=class_enumerators.MongoDatabase.DB_ADMIN.value,
    #     db_pass=class_enumerators.MongoDatabase.DB_PASSWORD.value,
    # )

    # for i,user in enumerate(client.docs):
    #     print(f'\n User {i+1}: ')
    #     pprint.pprint(user)