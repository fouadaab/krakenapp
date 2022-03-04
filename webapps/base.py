from fastapi import APIRouter
from webapps.auth import route_login

api_router = APIRouter()
api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])