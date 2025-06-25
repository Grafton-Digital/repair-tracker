from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routes import auth

app = FastAPI()
templates = Jinja2Templates(directory=Path("app") / "templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        name="views/index.jinja2",
        context={
            "request": request,
            "greeting": "Hello, World!"
        }
    )

app.include_router(auth.router, prefix="/auth")