from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.school import School, SchoolBase, SchoolUpdate, SchoolPublic, SchoolsPublic
from sqlmodel import select
from app.utils.dependencies import session_dep
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/", response_model=SchoolPublic)
def create_school(*, session: session_dep, school: SchoolBase):
    db_school = School.model_validate(school)
    session.add(db_school)
    session.commit()
    session.refresh(db_school)
    return db_school

@router.get("/", response_model=SchoolsPublic)
def list_schools(*, session: session_dep, request: Request):
    schools = session.exec(select(School)).all()
    return templates.TemplateResponse(
        "views/school_overview.html",
        {"request": request, "schools": schools}
    )

@router.get("/{school_id}", response_model=SchoolPublic)
def get_school(*, session: session_dep, school_id: uuid.UUID):
    school = session.get(School, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school

@router.get("/{school_id}/edit", response_model=SchoolPublic)
def edit_school(*, session: session_dep, school_id: uuid.UUID, request: Request):
    school = session.get(School, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return templates.TemplateResponse(
        "partials/school_edit.html",
        {"request": request, "school": school}
    )

@router.patch("/{school_id}", response_model=SchoolPublic)
def update_school(*, request: Request, session: session_dep, school_id: uuid.UUID, school_update: Annotated[SchoolUpdate, Form()]):
    db_school = session.get(School, school_id)
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")
    db_school.sqlmodel_update(school_update.model_dump(exclude_unset=True))
    session.add(db_school)
    session.commit()
    session.refresh(db_school)
    redirect_response = HTMLResponse(status_code=status.HTTP_200_OK)
    redirect_response.headers["HX-Redirect"] = "/school"  # For HTMX handling
    return redirect_response

# Come back and validate school has no repairs tied to it before deleting
@router.delete("/{school_id}", response_model=SchoolPublic)
def delete_school(*, session: session_dep, school_id: uuid.UUID):
    pass
    # db_school = session.get(SchoolBase, school_id)
    # if not db_school:
    #     raise HTTPException(status_code=404, detail="School not found")
    # session.delete(db_school)
    # session.commit()
    # return db_school