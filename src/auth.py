from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from src.config import SECRET_KEY, HASHING_ALGORITHM
from src.crud import get_user
from src.db import get_db
from src.models import UserDB
from src.utils import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=True)


def authenticate_user(db_session: Session, username: str, password: str):
    user = get_user(db_session=db_session, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    db_session: Session, data: dict, expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASHING_ALGORITHM)
    return encoded_jwt


async def get_current_user(
    db_session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = UserDB(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db_session=db_session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
