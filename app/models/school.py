from sqlmodel import SQLModel, Field
from typing import List, Optional
import uuid

class SchoolBase(SQLModel, table=True):
    __tablename__ = "schools",
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    contact_name: str = Field(max_length=255)
    address: str = Field(max_length=500)

class SchoolUpdate(SchoolBase):
    name: Optional[str] = Field(default=None, max_length=255)
    contact_name: Optional[str] = Field(default=None, max_length=255)
    address: Optional[str] = Field(default=None, max_length=500)

class SchoolPublic(SchoolBase):
    id: uuid.UUID

class SchoolsPublic(SQLModel):
    data: List[SchoolPublic]
    count: int