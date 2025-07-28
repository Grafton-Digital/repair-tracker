from fastapi import APIRouter, HTTPException
from app.models.school import School, SchoolBase, SchoolUpdate, SchoolPublic, SchoolsPublic
from sqlmodel import select
from app.utils.dependencies import session_dep
import uuid

router = APIRouter()

@router.post("/", response_model=SchoolPublic)
def create_school(*, session: session_dep, school: SchoolBase):
    db_school = School.model_validate(school)
    session.add(db_school)
    session.commit()
    session.refresh(db_school)
    return db_school

@router.get("/", response_model=SchoolsPublic)
def list_schools(*, session: session_dep):
    schools = session.exec(select(School)).all()
    return SchoolsPublic(data=schools, count=len(schools))

@router.get("/{school_id}", response_model=SchoolPublic)
def get_school(*, session: session_dep, school_id: uuid.UUID):
    school = session.get(School, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school

@router.patch("/{school_id}", response_model=SchoolPublic)
def update_school(*, session: session_dep, school_id: uuid.UUID, school_update: SchoolUpdate):
    db_school = session.get(School, school_id)
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")
    db_school.sqlmodel_update(school_update.model_dump(exclude_unset=True))
    session.add(db_school)
    session.commit()
    session.refresh(db_school)
    return db_school

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