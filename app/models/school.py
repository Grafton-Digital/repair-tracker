from sqlmodel import SQLModel, Field
from typing import List, Optional
import uuid

class SchoolBase(SQLModel):
    """Base model for schools"""
    name: str = Field()
    contact_name: str = Field()
    address: str = Field()

class School(SchoolBase, table=True):
    """School model for database"""
    __tablename__ = 'schools'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)

class SchoolUpdate(SchoolBase):
    name: Optional[str] = Field(default=None)
    contact_name: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)

class SchoolPublic(SchoolBase):
    id: uuid.UUID

class SchoolsPublic(SQLModel):
    data: List[SchoolPublic]
    count: int