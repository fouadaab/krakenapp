from apis.v1 import route_login, route_spent
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
api_router.include_router(route_spent.router, prefix="/spent", tags=["spent"])