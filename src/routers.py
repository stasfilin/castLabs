import secrets
import time
from datetime import timedelta, datetime

import aiohttp
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src import app, crud
from src.auth import authenticate_user, create_access_token, get_current_user
from src.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    HASHING_ALGORITHM,
)
from src.crud import add_http_proxy_result
from src.db import get_db
from src.models import UserDB, UserSchema, Token, ProxyDB, ProxySchema

router = APIRouter()


@router.get("/status")
async def status(*, db: Session = Depends(get_db)):
    result = crud.proxy_all(db_session=db)
    uptime = time.time() - app.app.extra["start_date"]
    return {"uptime": uptime, "processed": result}


@router.post("/user", response_model=UserDB, status_code=201)
async def create_user(*, db: Session = Depends(get_db), payload: UserSchema):
    try:
        user = crud.create_user(db_session=db, payload=payload)
        return user
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User Already Exists")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    *, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        db, data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", response_model=ProxyDB, status_code=201)
async def proxy(
    *,
    db: Session = Depends(get_db),
    payload: ProxySchema,
    current_user: UserDB = Depends(get_current_user)
):
    proxy_payload = {
        "iat": datetime.utcnow(),
        "jti": secrets.token_hex(32),
        "payload": {
            "user": current_user.username,
            "date": datetime.today().strftime("%Y-%m-%d"),
        },
    }
    token = jwt.encode(proxy_payload, SECRET_KEY, algorithm=HASHING_ALGORITHM)

    async with aiohttp.ClientSession() as session:
        try:
            response = await session.post(payload.link, headers={"x-my-jwt": token},)
            if response.status == 200:
                add_http_proxy_result(db, payload, current_user, True)
                return {"is_done": True, "link": payload.link}
            else:
                add_http_proxy_result(db, payload, current_user, False)
                return {"is_done": False, "link": payload.link}
        except (aiohttp.ClientConnectionError, aiohttp.client_exceptions.InvalidURL):
            add_http_proxy_result(db, payload, current_user, False)
            return {"is_done": False, "link": payload.link}
