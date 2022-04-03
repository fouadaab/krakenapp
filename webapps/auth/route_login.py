from apis.v1.route_login import login_for_access_token
from apis.v1.route_login import get_current_user
from apis.v1.route_user import query_or_cookie_extractor
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from webapps.auth.forms import LoginForm

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)
users = []

@router.get("/login/")
def login(request: Request, cookie: str = Depends(query_or_cookie_extractor)):
    if cookie:
        current_user = get_current_user(cookie)
        if current_user not in users:
            users.append(current_user)
        response =  RedirectResponse(url=f'/dash')
        return response
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login/")
async def login(request: Request):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful!")
            response =  RedirectResponse(url=f'/dash')
            token = login_for_access_token(response=response, form_data=form)
            cookie_value = token.get('access_token')
            current_user = get_current_user(cookie_value)
            if current_user not in users:
                users.append(current_user)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)