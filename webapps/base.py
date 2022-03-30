from fastapi import APIRouter
from webapps.auth import route_login, route_user
from app.dashapp.app import mount_dash

api_router = APIRouter()
api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])
api_router.include_router(route_user.router, prefix="", tags=["user-webapp"])

from kraken_main import app
mount_dash(app, cookie=route_login.cookie_global)
