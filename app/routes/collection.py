from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.models.collection import CollectionBase, CollectionCreate, CollectionUpdate, CollectionPublic, CollectionsPublic
from app.utils.dependencies import session_dep
import uuid

router = APIRouter()

@router.post("/", response_model=CollectionPublic)
def create_collection(*, session: session_dep, collection: CollectionCreate):
    db_collection = CollectionBase.model_validate(collection)
    session.add(db_collection)
    session.commit()
    session.refresh(db_collection)
    return db_collection

@router.get("/", response_model=CollectionsPublic)
def list_collections(*, session: session_dep):
    collections = session.exec(select(CollectionBase)).all()
    return CollectionsPublic(data=collections, count=len(collections))

@router.get("/{collection_id}", response_model=CollectionPublic)
def get_collection(*, session: session_dep, collection_id: uuid.UUID):
    collection = session.get(CollectionBase, collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

@router.patch("/{collection_id}", response_model=CollectionPublic)
def update_collection(*, session: session_dep, collection_id: uuid.UUID, collection_update: CollectionUpdate):
    db_collection = session.get(CollectionBase, collection_id)
    if not db_collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    db_collection.sqlmodel_update(collection_update.model_dump(exclude_unset=True))
    session.add(db_collection)
    session.commit()
    session.refresh(db_collection)
    return db_collection

@router.delete("/{collection_id}", response_model=CollectionPublic)
def delete_collection(*, session: session_dep, collection_id: uuid.UUID):
    db_collection = session.get(CollectionBase, collection_id)
    if not db_collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    session.delete(db_collection)
    session.commit()
    return db_collection
