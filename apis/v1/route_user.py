from fastapi import Depends, Cookie
from typing import Optional


async def query_extractor(access_token: Optional[str] = Cookie(None)):
    return access_token


async def query_or_cookie_extractor(
    q: str = Depends(query_extractor), last_query: Optional[str] = ''
):
    if not q:
        return last_query
    return q