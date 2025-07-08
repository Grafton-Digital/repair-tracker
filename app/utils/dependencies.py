from collections.abc import Generator
from typing import Annotated
import uuid

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyCookie
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.config import settings
from app.database import engine
from app.models.user import TokenPayload, User

apikey_cookie = APIKeyCookie(name="access_token", auto_error=False)
token_dep = Annotated[str, Depends(apikey_cookie)]

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

session_dep = Annotated[Session, Depends(get_db)]

def get_current_user(session: session_dep, token: token_dep, request: Request) -> User:
    # If access token cookie is not present, redirect to login
    try:
        if token:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            token_data = TokenPayload(**payload)
        else:
            raise NameError("Access token not found")

        if not (user := session.get(User, uuid.UUID(token_data.sub))):
            raise NameError("User not found")
        
        if not user.is_active:
            raise ValueError("Inactive user")

        return user
        
    except (InvalidTokenError, ValidationError, NameError, ValueError):
        # Redirect to login with ?next=original_path
        login_url = f"/auth/login?next={request.url.path}"
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": login_url},
            detail="Not Authenticated",
        )

user_dep = Annotated[User, Depends(get_current_user)]

def get_current_active_superuser(current_user: user_dep) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    return current_user

superuser_dep = Annotated[User, Depends(get_current_active_superuser)]