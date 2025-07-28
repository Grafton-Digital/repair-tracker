from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.models.note import Note, NoteBase, NotePublic, NoteUpdate, NotesPublic
from app.utils.dependencies import session_dep, user_dep
import uuid

router = APIRouter()

@router.post("/", response_model=NotePublic)
def create_note(*, session: session_dep, user: user_dep, note: NoteBase):
    db_note = Note.model_validate(note, update={"creator_id": user.id})
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note

@router.get("/", response_model=NotesPublic)
def list_notes(*, session: session_dep):
    notes = session.exec(select(Note)).all()
    return NotesPublic(data=notes, count=len(notes))

@router.get("/{note_id}", response_model=NotePublic)
def get_note(*, session: session_dep, note_id: uuid.UUID):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.patch("/{note_id}", response_model=NotePublic)
def update_note(*, session: session_dep, note_id: uuid.UUID, note_update: NoteUpdate):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db_note.sqlmodel_update(note_update.model_dump(exclude_unset=True))
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note

@router.delete("/{note_id}", response_model=NotePublic)
def delete_note(*, session: session_dep, note_id: uuid.UUID):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(db_note)
    session.commit()
    return db_note
