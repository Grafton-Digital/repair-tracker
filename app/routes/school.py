from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.repair import Repair
from app.models.school import School, SchoolBase, SchoolUpdate
from sqlmodel import select
from app.utils.dependencies import session_dep
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

#
# School view routes and HTMX Partials
#

@router.get("/overview", response_class=HTMLResponse)
def school_overview(*, session: session_dep, request: Request):
    schools = session.exec(select(School)).all()
    return templates.TemplateResponse(
        "components/school_overview.html",
        {"request": request, "schools": schools}
    )

@router.get("/new", response_class=HTMLResponse)
def new_school(*, request: Request):
    return templates.TemplateResponse(
        "views/school_new.html",
        {"request": request}
    )

@router.get("/{school_id}/edit", response_class=HTMLResponse)
def edit_school(*, session: session_dep, school_id: uuid.UUID, request: Request):
    school = session.get(School, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return templates.TemplateResponse(
        "partials/school_edit.html",
        {"request": request, "school": school}
    )

# 
# School CRUD routes
#

@router.post("/", response_class=HTMLResponse)
def create_school(*, request: Request, session: session_dep, school: Annotated[SchoolBase, Form()]):
    db_school = School.model_validate(school)
    session.add(db_school)
    session.commit()
    session.refresh(db_school)
    return templates.TemplateResponse(
        name="components/notification.html",
        context={"request": request, "message": "School created successfully!", "type": "success"},
        status_code=status.HTTP_201_CREATED,
        headers={"HX-Trigger": "refreshOverview"}
    )

@router.patch("/{school_id}", response_class=HTMLResponse)
def update_school(*, session: session_dep, school_id: uuid.UUID, school_update: Annotated[SchoolUpdate, Form()]):
    db_school = session.get(School, school_id)
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")
    db_school.sqlmodel_update(school_update.model_dump(exclude_unset=True))
    session.add(db_school)
    session.commit()
    session.refresh(db_school)
    return HTMLResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "HX-Trigger": "refreshOverview"
        }
    )

@router.delete("/{school_id}", response_class=HTMLResponse)
def delete_school(*, request: Request, session: session_dep, school_id: uuid.UUID):
    associated_repairs = session.exec(
        select(Repair).where(Repair.school_id == school_id)
    ).all()

    if associated_repairs:
        return templates.TemplateResponse(
            "components/notification.html",
            {"request": request, "message": "Cannot delete a school with associated repairs!", "type": "error"}
        )
    
    db_school = session.get(School, school_id)
    if not db_school:
        return templates.TemplateResponse(
            "components/notification.html",
            {"request": request, "message": "Cannot delete a school that does not exist!", "type": "error"}
        )
    
    session.delete(db_school)
    session.commit()
    return templates.TemplateResponse(
        name="components/notification.html",
        context={"request": request, "message": "School successfully deleted!", "type": "success"},
        headers={"HX-Trigger": "refreshOverview"}
    )

# NOT IN USE YET
# Might want this to be a row partial or a card or something
# @router.get("/{school_id}", response_model=SchoolPublic)
# def get_school(*, session: session_dep, school_id: uuid.UUID):
#     school = session.get(School, school_id)
#     if not school:
#         raise HTTPException(status_code=404, detail="School not found")
#     return school