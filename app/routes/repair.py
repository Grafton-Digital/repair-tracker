from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from app.models.repair import Repair, RepairBase, RepairCreate, RepairUpdate, RepairPublic, RepairsPublic
from app.utils.dependencies import session_dep, user_dep
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/", response_model=RepairPublic)
def create_repair(*, session: session_dep, user: user_dep, repair: RepairCreate):
    db_repair = Repair.model_validate(repair, update={"creator_id": user.id})
    session.add(db_repair)
    session.commit()
    session.refresh(db_repair)
    return db_repair

@router.get("/", response_class=HTMLResponse)
def repairs_page(request: Request, session: session_dep):
    # Get 10 most recent repairs
    repairs = session.exec(
        select(Repair).order_by(Repair.created_at.desc()).limit(10)
    ).all()
    return templates.TemplateResponse(
        "components/repair_overview.html", 
        {"request": request, "repairs": repairs}
    )

@router.get("/all", response_model=RepairsPublic)
def list_repairs(*, session: session_dep, limit: int = None):
    query = select(Repair).order_by(Repair.created_at.desc())
    if limit:
        query = query.limit(limit)
    repairs = session.exec(query).all()
    return RepairsPublic(data=repairs, count=len(repairs))

@router.get("/{repair_id}", response_model=RepairPublic)
def get_repair(*, session: session_dep, repair_id: uuid.UUID):
    repair = session.get(Repair, repair_id)
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    return repair

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