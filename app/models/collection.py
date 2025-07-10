from sqlmodel import SQLModel, Field
from typing import List, Optional
import uuid

class CollectionBase(SQLModel, table=True):
    __tablename__ = "collections"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    origin: Optional[str] = Field(default=None, max_length=255)
    destination: Optional[str] = Field(default=None, max_length=255)
    collection_number: str = Field(max_length=100)

class CollectionCreate(CollectionBase):
    repair_id: uuid.UUID

class CollectionUpdate(CollectionBase):
    origin: Optional[str] = Field(default=None, max_length=255)
    destination: Optional[str] = Field(default=None, max_length=255)
    collection_number: Optional[str] = Field(default=None, max_length=100)

class CollectionPublic(CollectionBase):
    id: uuid.UUID
    repair_id: uuid.UUID

class CollectionsPublic(SQLModel):
    data: List[CollectionPublic]
    count: int