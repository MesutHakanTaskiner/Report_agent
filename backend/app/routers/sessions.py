from fastapi import APIRouter, HTTPException, status, Depends, Response
from typing import List
from sqlalchemy.orm import Session as SQLAlchemySession
from datetime import datetime

from app.models.schemas import Session as SessionSchema, SessionCreate
from app.models.database import Session as SessionModel
from app.utils.database import get_db

router = APIRouter()

@router.get("/", response_model=List[SessionSchema])
async def get_sessions(db: SQLAlchemySession = Depends(get_db)):
    """Get all sessions"""
    sessions = db.query(SessionModel).all()
    return sessions

@router.get("/{session_id}", response_model=SessionSchema)
async def get_session(session_id: str, db: SQLAlchemySession = Depends(get_db)):
    """Get a specific session by ID"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found"
        )
    return session

@router.post("/", response_model=SessionSchema, status_code=status.HTTP_201_CREATED)
async def create_session(session: SessionCreate, db: SQLAlchemySession = Depends(get_db)):
    """Create a new session"""
    new_session = SessionModel.create_new(title=session.title)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.put("/{session_id}", response_model=SessionSchema)
async def update_session(session_id: str, session: SessionCreate, db: SQLAlchemySession = Depends(get_db)):
    """Update a session"""
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found"
        )
    
    # Update session title
    db_session.title = session.title
    db.commit()
    db.refresh(db_session)
    return db_session

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str, db: SQLAlchemySession = Depends(get_db)):
    """Delete a session"""
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found"
        )
    
    # Delete session (cascade will delete related messages)
    db.delete(db_session)
    db.commit()
    return None

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_sessions(db: SQLAlchemySession = Depends(get_db)):
    """Delete all sessions"""
    # Delete all sessions (cascade will delete related messages)
    db.query(SessionModel).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{session_id}/favorite", response_model=SessionSchema)
async def toggle_favorite(session_id: str, db: SQLAlchemySession = Depends(get_db)):
    """Toggle the favorite status of a session"""
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found"
        )
    
    # Toggle favorite status
    db_session.isFavorite = not db_session.isFavorite
    db.commit()
    db.refresh(db_session)
    return db_session
