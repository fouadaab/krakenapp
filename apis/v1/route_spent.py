from fastapi import Depends, Cookie
from fastapi import APIRouter
from typing import Optional


router = APIRouter()


def query_extractor(access_token: Optional[str] = Cookie(None)):
    return access_token


def query_or_cookie_extractor(
    q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)
):
    if not q:
        return last_query  # Add rejection here -> Not authorized etc.
    return q