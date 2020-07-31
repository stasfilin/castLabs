from sqlalchemy.orm import Session

from src.models import User, UserSchema, ProxySchema, HTTPProxy, UserDB
from src.utils import get_password_hash


def create_user(db_session: Session, payload: UserSchema):
    hashed_password = get_password_hash(payload.password)
    user = User(username=payload.username, hashed_password=hashed_password)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def get_user(db_session: Session, username: str):
    return db_session.query(User).filter(User.username == username).first()


def add_http_proxy_result(
    db_session: Session, payload: ProxySchema, user: UserDB, status: bool = False
):
    result = HTTPProxy(user_id=user.id, link=payload.link, is_done=status)
    db_session.add(result)
    db_session.commit()
    db_session.refresh(result)
    return result


def proxy_all(db_session: Session):
    return db_session.query(HTTPProxy).count()
