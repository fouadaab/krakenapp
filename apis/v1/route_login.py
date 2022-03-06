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
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from schemas.tokens import Token, TokenData
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    _id: int
    userid: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    password: str


def get_user(username: str):
    client = MongoDB()
    client.db_find_user(
        db_name=settings.DB_NAME,
        db_col=settings.DB_COLLECTION,
        db_admin=settings.DB_ADMIN,
        db_pass=settings.DB_PASSWORD,
        username=username,
    )
    user_dict = client.user
    if user_dict:
        return UserInDB(**user_dict)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token.replace(settings.TOKEN_BEARER_TAG,''),
            settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
        username: str = payload.get("user")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

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
        data={"user": user.username}, expires_delta=access_token_expires
    )
    response.status_code = 302
    response.set_cookie(
        key="access_token", value=settings.TOKEN_BEARER_TAG+access_token, httponly=True, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    return {"access_token": access_token, "token_type": "bearer"}