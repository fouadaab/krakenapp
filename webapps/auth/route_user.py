from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from apis.v1.route_user import query_or_cookie_extractor
from apis.v1.route_login import get_current_user


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/user")
async def read_user_token(cookie: str = Depends(query_or_cookie_extractor)):
    if not cookie:
        response =  RedirectResponse(url='/login')
        return response
    user = get_current_user(cookie)
    return {"user token": user}
