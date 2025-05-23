from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi_htmx import htmx, htmx_init

app = FastAPI()
templates = Jinja2Templates(directory=Path("app") / "templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        name="views/index.jinja2",
        context={
            "request": request,
            "greeting": "Hello, World!"
        }
    )