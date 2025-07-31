from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import or_, select
from app.models.collection import Collection, CollectionBase, CollectionPublic, CollectionsPublic
from app.models.repair import Repair
from app.utils.dependencies import session_dep
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

#
# Device view routes and HTMX Partials
#

@router.get("/overview", response_class=HTMLResponse)
def collection_overview(*, session: session_dep, request: Request):
    collections = session.exec(select(Collection)).all()
    return templates.TemplateResponse(
        "views/collection_overview.html",
        {"request": request, "collections": collections}
    )

#
# Collection CRUD routes
#

@router.post("/", response_class=HTMLResponse)
def create_collection(*, request: Request, session: session_dep, collection: Annotated[CollectionBase, Form()]):
    db_collection = Collection.model_validate(collection)
    session.add(db_collection)
    session.commit()
    session.refresh(db_collection)
    return templates.TemplateResponse(
        name="components/notification.html",
        context={"request": request, "message": "Collection created successfully!", "type": "success"},
        headers={"HX-Trigger": "refreshOverview"},
        status_code=status.HTTP_201_CREATED
    )

@router.delete("/{collection_id}", response_model=CollectionPublic)
def delete_collection(*, request: Request, session: session_dep, collection_id: uuid.UUID):
    associated_repairs = session.exec(
        select(Repair)
        .where(
            or_(
                Repair.inbound_collection_id == collection_id,
                Repair.outbound_collection_id == collection_id
            )
        )
    ).all()

    if associated_repairs:
        return templates.TemplateResponse(
            "components/notification.html",
            {"request": request, "message": "Cannot delete collection with associated repairs.", "type": "error"},
        )
    
    db_collection = session.get(Collection, collection_id)
    if not db_collection:
        return templates.TemplateResponse(
            "components/notification.html",
            {"request": request, "message": "Cannot delete a collection that does not exist!", "type": "error"},
        )
    
    session.delete(db_collection)
    session.commit()
    return templates.TemplateResponse(
        "components/notification.html",
        {"request": request, "message": "Collection deleted successfully!", "type": "success"},
        headers={"HX-Trigger": "refreshOverview"}
    )

# TO-DO: Check with Wayne if collections should be updatable
# @router.patch("/{collection_id}", response_model=CollectionPublic)
# def update_collection(*, session: session_dep, collection_id: uuid.UUID, collection_update: CollectionUpdate):
#     pass
    # db_collection = session.get(CollectionBase, collection_id)
    # if not db_collection:
    #     raise HTTPException(status_code=404, detail="Collection not found")
    # db_collection.sqlmodel_update(collection_update.model_dump(exclude_unset=True))
    # session.add(db_collection)
    # session.commit()
    # session.refresh(db_collection)
    # return db_collection

# Not in use yet
# @router.get("/{collection_id}", response_model=CollectionPublic)
# def get_collection(*, session: session_dep, collection_id: uuid.UUID):
#     collection = session.get(Collection, collection_id)
#     if not collection:
#         raise HTTPException(status_code=404, detail="Collection not found")
#     return collection