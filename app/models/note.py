from sqlmodel import SQLModel, Field
from typing import List
import uuid

class NoteBase(SQLModel):
    """Base model for notes"""
    creator_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    repair_id: uuid.UUID = Field(foreign_key="repairs.id", nullable=False)
    text: str = Field(max_length=2000)

class Note(NoteBase, table=True):
    """Note model for database"""
    __tablename__ = "notes"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class NotePublic(NoteBase):
    """Public model for notes"""
    id: uuid.UUID

class NoteUpdate(SQLModel):
    text: str = Field(max_length=4000)

class NotesPublic(SQLModel):
    data: List[NotePublic]
    count: int