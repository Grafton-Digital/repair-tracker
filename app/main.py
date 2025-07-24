from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routes import auth, repair
from app.utils.dependencies import user_dep

app = FastAPI()
templates = Jinja2Templates(directory=Path("app") / "templates")

@app.get("/", response_class=HTMLResponse)
async def renderIndex(request: Request, current_user: user_dep):
    return templates.TemplateResponse(
        name="views/index.html",
        context={
            "request": request,
            "greeting": f"Hello {current_user.full_name or "Unknown Person"}!"
        }
    )

app.include_router(auth.router, prefix="/auth")
app.include_router(repair.router, prefix="/repair")