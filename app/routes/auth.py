from datetime import datetime, timedelta, timezone
from pathlib import Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException, Request, Response, Query, status
from typing import Annotated, Any

from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from app.config import settings
import jwt

from app.models.user import User, UserCreate, UserPublic, UserRegister, get_user_by_email, create_user
from app.utils.dependencies import session_dep
from app.utils.security import verify_password

templates = Jinja2Templates(directory=Path("app") / "templates")

def authenticate(session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def renderLogin(request: Request, next: str = Query(default="/")):
    """
    Render the login page.
    """
    return templates.TemplateResponse(
        name="views/login.html",
        context={
            "request": request,
            "next": next
        }
    )

@router.post("/login", response_class=RedirectResponse)
def login(
    response: Response,
    session: session_dep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    next: str = Query(default="/")
):
    user = authenticate(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.id, expires_delta=access_token_expires)
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    # Redirect to the original page after login
    response.headers["Location"] = next
    response.status_code = status.HTTP_303_SEE_OTHER
    return response

@router.get("/register")
def renderRegister():
    pass

@router.post("/register", response_model=UserPublic)
def register(session: session_dep, new_user: UserRegister):
    """
    Create new user without needing to be logged in (e.g. as a Superuser)
    """
    # Check if user with the same email already exists
    existing_user = get_user_by_email(session=session, email=new_user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email already exists")

    # Create a new user with sane default values for is_superuser and is_active
    user_create = UserCreate.model_validate(
        new_user,
        update={"is_superuser": False, "is_active": True}
    )
    user = create_user(session=session, user_create=user_create)
    return user
