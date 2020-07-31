from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.db import Base


class User(Base):

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("username",),)

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    hashed_password = Column(String(100))

    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password


class UserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=3, max_length=100)


class UserDB(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class HTTPProxy(Base):

    __tablename__ = "proxy"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User)
    link = Column(String(50))
    is_done = Column(Boolean, default=True)

    def __init__(self, user_id, link, is_done):
        self.user_id = user_id
        self.link = link
        self.is_done = is_done


class ProxySchema(BaseModel):
    link: str = Field(
        min_length=3, max_length=50, example="https://postman-echo.com/post/"
    )


class ProxyDB(BaseModel):
    link: str = Field(..., min_length=3, max_length=50)
    is_done: bool = Field()

    class Config:
        orm_mode = True
