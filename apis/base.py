from apis.v1 import route_login, route_user
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
api_router.include_router(route_user.router, prefix="/user", tags=["user"])