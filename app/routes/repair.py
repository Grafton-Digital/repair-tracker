from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from app.models.note import Note
from app.models.repair import Repair, RepairBase, RepairCreate, RepairUpdate, RepairPublic
from app.utils.dependencies import session_dep, user_dep
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

#
# Repair view routes and HTMX partials
#

@router.get("/overview", response_class=HTMLResponse)
def repairs_page(request: Request, session: session_dep):
    repairs = session.exec(
        select(Repair).order_by(Repair.created_at.desc()).limit(10)
    ).all()
    return templates.TemplateResponse(
        "views/repair_overview.html", 
        {"request": request, "repairs": repairs}
    )

@router.get("/new", response_class=HTMLResponse)
def new_repair(*, request: Request):
    return templates.TemplateResponse(
        "partials/repair_new.html",
        {"request": request}
    )

@router.get("/{repair_id}/edit", response_class=HTMLResponse)
def edit_repair(*, session: session_dep, repair_id: uuid.UUID, request: Request):
    repair = session.get(Repair, repair_id)
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    return templates.TemplateResponse(
        "partials/repair_edit.html",
        {"request": request, "repair": repair}
    )

#
# Repair CRUD routes
#

@router.post("/", response_class=HTMLResponse)
def create_repair(*, request: Request, response: Response, session: session_dep, user: user_dep, repair: Annotated[RepairCreate, Form()]):
    db_repair = Repair.model_validate(repair, update={"creator_id": user.id})
    session.add(db_repair)
    session.commit()
    session.refresh(db_repair)
    return templates.TemplateResponse(
        "components/notification.html",
        {"request": request, "message": "Repair created successfully!", "type": "success"},
        status_code=status.HTTP_201_CREATED,
        headers={"HX-Trigger": "refreshOverview"}
    )

@router.get("/{repair_id}", response_class=HTMLResponse)
def get_repair(*, request: Request, session: session_dep, repair_id: uuid.UUID):
    repair = session.get(Repair, repair_id)
    notes = session.exec(
        select(Note).where(Note.repair_id == repair_id).order_by(Note.created_at.desc())
    ).all()
    if not repair:
        return templates.TemplateResponse(
            "components/notification.html",
            {"request": request, "message": "Repair not found", "type": "error"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return templates.TemplateResponse(
        "views/repair_view.html",
        {"request": request, "repair": repair, "notes": notes}
    )

@router.patch("/{repair_id}", response_model=RepairPublic)
def update_repair(*, session: session_dep, repair_id: uuid.UUID, repair_update: RepairUpdate):
    db_repair = session.get(RepairBase, repair_id)
    if not db_repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    db_repair.sqlmodel_update(repair_update.model_dump(exclude_unset=True))
    session.add(db_repair)
    session.commit()
    session.refresh(db_repair)
    return db_repair