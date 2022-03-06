from fastapi import APIRouter
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from apis.v1.route_spent import query_or_cookie_extractor


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/spent/{currency}/")
async def read_item(currency: str, query_or_default: str = Depends(query_or_cookie_extractor)):
    cookie = query_or_default
    return {"sum spent in": currency, "cookie": cookie}
