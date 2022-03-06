from fastapi import APIRouter, Depends
from webapps.auth import route_login, route_spent


api_router = APIRouter()
api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])
api_router.include_router(route_spent.router, prefix="", tags=["spent-webapp"])