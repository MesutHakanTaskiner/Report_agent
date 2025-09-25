from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
import uuid
import os
from datetime import datetime
import asyncio
from sqlalchemy.orm import Session as SQLAlchemySession

from app.models.schemas import Message as MessageSchema, MessageCreate, FileAttachment as FileAttachmentSchema
from app.models.database import Message as MessageModel, Session as SessionModel, FileAttachment as FileAttachmentModel
from app.utils.database import get_db, SessionLocal
from app.services.openai_service import analyze_files, generate_conversation_response

router = APIRouter()

@router.get("/{session_id}", response_model=List[MessageSchema])
async def get_messages(session_id: str, db: SQLAlchemySession = Depends(get_db)):
    """Get all messages for a specific session"""
    # Check if session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found"
        )
    
    # Get all messages for the session
    messages = db.query(MessageModel).filter(MessageModel.session_id == session_id).all()
    return messages

@router.post("/{session_id}", response_model=MessageSchema, status_code=status.HTTP_201_CREATED)
async def create_message(session_id: str, message: MessageCreate, db: SQLAlchemySession = Depends(get_db)):
    """Create a new message in a session"""
    # Check if session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found"
        )
    
    # Create user message
    new_message = MessageModel.create_new(
        role=message.role,
        content=message.content,
        session_id=session_id,
        analysis_type=message.analysis_type
    )
    
    # Add attachments if present
    if message.attachments:
        for attachment_data in message.attachments:
            # Find the attachment in the database
            attachment = db.query(FileAttachmentModel).filter(FileAttachmentModel.id == attachment_data.id).first()
            if attachment:
                new_message.attachments.append(attachment)
        
        # Update file count
        session.fileCount += len(message.attachments)
    
    # Save the message
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    # Generate assistant response using OpenAI
    asyncio.create_task(create_assistant_response(
        session_id, 
        message.content, 
        message.analysis_type, 
        message.attachments,
        db
    ))
    
    return new_message

async def create_assistant_response(session_id: str, user_message: str, analysis_type: str = None, attachments = None, db: SQLAlchemySession = None):
    """Create an assistant response after analyzing the request"""
    # Create a new database session if not provided
    db_factory = None
    if db is None:
        db_factory = SessionLocal()
        try:
            db = db_factory
        except Exception as e:
            print(f"Error creating database session: {e}")
            return
    
    try:
        # First create a "thinking" message
        thinking_message = MessageModel.create_new(
            role="assistant",
            content="I'm analyzing your request...",
            session_id=session_id,
            analysis_type=analysis_type
        )
        thinking_message.isStreaming = True
        
        db.add(thinking_message)
        db.commit()
        db.refresh(thinking_message)
        thinking_id = thinking_message.id
        
        # Check if there are files to analyze
        file_paths = []
        if attachments:
            print(f"Processing {len(attachments)} attachments")
            for attachment in attachments:
                file_id = attachment.id
                
                # Check if the file exists in the database
                file_attachment = db.query(FileAttachmentModel).filter(FileAttachmentModel.id == file_id).first()
                if file_attachment:
                    file_name = file_attachment.name
                    file_path = os.path.join(
                        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                        "uploads", 
                        f"{file_id}_{file_name}"
                    )
                    
                    # Check if the file exists on disk
                    if os.path.exists(file_path):
                        file_paths.append(file_path)
                        print(f"Found existing file: {file_path}")
                    else:
                        print(f"Warning: File {file_id}_{file_name} not found on disk")
                else:
                    print(f"Warning: File with ID {file_id} not found in database")
        
        # Prepare conversation history for context
        conversation_history = []
        # Get previous messages from this session (limited to last 10 to avoid token limits)
        previous_messages = db.query(MessageModel).filter(
            MessageModel.session_id == session_id,
            MessageModel.id != thinking_id
        ).order_by(MessageModel.timestamp.desc()).limit(10).all()
        
        for msg in reversed(previous_messages):  # Reverse to get chronological order
            conversation_history.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Generate response based on files and analysis type
        if file_paths:
            # Use OpenAI to analyze files
            response_content = await analyze_files(
                file_paths=file_paths,
                analysis_type=analysis_type or "summarize",
                user_message=user_message
            )
        else:
            # No files to analyze, use conversation-based response
            response_content = await generate_conversation_response(
                conversation_history=conversation_history,
                user_message=user_message
            )
        
        # Update the thinking message with the actual response
        thinking_message = db.query(MessageModel).filter(MessageModel.id == thinking_id).first()
        if thinking_message:
            thinking_message.content = response_content
            thinking_message.isStreaming = False
            db.commit()
    
    except Exception as e:
        print(f"Error in create_assistant_response: {e}")
    
    finally:
        # Close the database session if we created it
        if db is not None and db_factory is not None:
            db_factory.close()
