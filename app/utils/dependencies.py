from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.config import settings
from app.database import engine
from app.models.user import TokenPayload, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
token_dep = Annotated[str, Depends(oauth2_scheme)]

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

session_dep = Annotated[Session, Depends(get_db)]

def get_current_user(session: session_dep, token: token_dep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

user_dep = Annotated[User, Depends(get_current_user)]

def get_current_active_superuser(current_user: user_dep) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user

superuser_dep = Annotated[User, Depends(get_current_active_superuser)]