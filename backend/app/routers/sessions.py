from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from datetime import datetime

from app.models.schemas import Session, SessionCreate
from app.utils.database import sessions_db, messages_db

router = APIRouter()

@router.get("/", response_model=List[Session])
async def get_sessions():
    """Get all sessions"""
    return list(sessions_db.values())

@router.get("/{session_id}", response_model=Session)
async def get_session(session_id: str):
    """Get a specific session by ID"""
    if session_id not in sessions_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found"
        )
    return sessions_db[session_id]

@router.post("/", response_model=Session, status_code=status.HTTP_201_CREATED)
async def create_session(session: SessionCreate):
    """Create a new session"""
    session_id = str(uuid.uuid4())
    new_session = Session(
        id=session_id,
        title=session.title,
        timestamp=datetime.now(),
        fileCount=0,
        isFavorite=False
    )
    sessions_db[session_id] = new_session
    messages_db[session_id] = []
    return new_session

@router.put("/{session_id}", response_model=Session)
async def update_session(session_id: str, session: SessionCreate):
    """Update a session"""
    if session_id not in sessions_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found"
        )
    
    existing_session = sessions_db[session_id]
    updated_session = Session(
        id=session_id,
        title=session.title,
        timestamp=existing_session.timestamp,
        fileCount=existing_session.fileCount,
        isFavorite=existing_session.isFavorite
    )
    sessions_db[session_id] = updated_session
    return updated_session

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str):
    """Delete a session"""
    if session_id not in sessions_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found"
        )
    
    del sessions_db[session_id]
    if session_id in messages_db:
        del messages_db[session_id]
    return None

@router.put("/{session_id}/favorite", response_model=Session)
async def toggle_favorite(session_id: str):
    """Toggle the favorite status of a session"""
    if session_id not in sessions_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found"
        )
    
    session = sessions_db[session_id]
    session.isFavorite = not session.isFavorite
    return session
