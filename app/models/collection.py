from sqlmodel import SQLModel, Field
from typing import List
import uuid

class CollectionBase(SQLModel):
	"""Base model for collections"""
	collection_number: str = Field(max_length=100)
	origin: str = Field(default=None)
	destination: str = Field(default=None)
	repair_id: uuid.UUID = Field(foreign_key="repairs.id", nullable=False)	

class Collection(CollectionBase, table=True):
	"""Collection model for database"""
	__tablename__ = 'collections'
	id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
	repair_id: uuid.UUID = Field(foreign_key="repairs.id", nullable=False)

class CollectionPublic(CollectionBase):
    """Public model for collections"""
    id: uuid.UUID

class CollectionsPublic(SQLModel):
    """Public model for fetching a list of collections with count"""
    data: List[CollectionPublic]
    count: int