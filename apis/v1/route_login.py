from datetime import timedelta
from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token
from db.db_client import MongoDB
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.tokens import Token

router = APIRouter()

def authenticate_user(username: str, password: str):
    client = MongoDB()
    client.db_find_user(
        db_name=settings.DB_NAME,
        db_col=settings.DB_COLLECTION,
        db_admin=settings.DB_ADMIN,
        db_pass=settings.DB_PASSWORD,
        username=username,
    )
    user = client.user
    if not user:
        return False
    if not Hasher.verify_password(password, user['password']):
        return False
    return user

@router.post("/token", response_model=Token)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}