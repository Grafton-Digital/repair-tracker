from sqlmodel import SQLModel, Field
from typing import List
import uuid

class NoteBase(SQLModel):
    """Base model for notes"""
    repair_id: uuid.UUID = Field(foreign_key="repairs.id", nullable=False)
    text: str = Field(max_length=4000)

class Note(NoteBase, table=True):
    """Note model for database"""
    __tablename__ = "notes"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    creator_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)

class NotePublic(NoteBase):
    """Public model for notes"""
    id: uuid.UUID
    creator_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)

class NoteUpdate(SQLModel):
    text: str = Field(max_length=4000)

class NotesPublic(SQLModel):
    data: List[NotePublic]
    count: int