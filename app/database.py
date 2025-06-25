from typing import Annotated
from sqlmodel import Session, create_engine
from fastapi import Depends
from app.config import settings

from app import models

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

SessionDep = Annotated[Session, Depends(get_session)]