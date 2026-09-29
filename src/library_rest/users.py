import uuid
from typing import Literal, Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from library_rest.models import User
from library_rest.db import get_user_db
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
SECRET = os.getenv("SECRET_KEY")

class UserRead(BaseUser[uuid.UUID]):
    pass

class UserCreate(BaseUserCreate):
    is_active: Literal[True] = True
    is_superuser: Literal[False] = False
    is_verified: Literal[False] = False

class UserUpdate(BaseUserUpdate):
    pass

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        return {"details": "Usuario registrado!"}

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_superUser = fastapi_users.current_user(active=True, superuser=True)

