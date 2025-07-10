from .user import UserPublic

from sqlmodel import SQLModel, Field
from typing import List, Optional
import uuid

class NoteBase(SQLModel, table=True):
    """Base model for notes"""
    __tablename__ = "notes"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    creator_id: uuid.UUID
    repair_id: uuid.UUID
    text: str = Field(max_length=2000)

class NoteCreate(NoteBase):
    repair_id: uuid.UUID

class NoteUpdate(NoteBase):
    text: Optional[str] = Field(default=None, max_length=2000)

class NoteWithCreator(NoteBase):
    """Note with creator information"""
    creator: Optional["UserPublic"] = None

class NotesPublic(SQLModel):
    data: List[NoteBase]
    count: int