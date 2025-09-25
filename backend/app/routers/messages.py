from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
import os
from datetime import datetime
import asyncio

from app.models.schemas import Message, MessageCreate, FileAttachment
from app.utils.database import messages_db, sessions_db, files_db
from app.services.openai_service import analyze_files, generate_conversation_response

router = APIRouter()

@router.get("/{session_id}", response_model=List[Message])
async def get_messages(session_id: str):
    """Get all messages for a specific session"""
    if session_id not in sessions_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found"
        )
    
    if session_id not in messages_db:
        messages_db[session_id] = []
    
    return messages_db[session_id]

@router.post("/{session_id}", response_model=Message, status_code=status.HTTP_201_CREATED)
async def create_message(session_id: str, message: MessageCreate):
    """Create a new message in a session"""
    if session_id not in sessions_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found"
        )
    
    if session_id not in messages_db:
        messages_db[session_id] = []
    
    # Create user message
    message_id = str(uuid.uuid4())
    new_message = Message(
        id=message_id,
        role=message.role,
        content=message.content,
        timestamp=datetime.now(),
        attachments=message.attachments,
        status="sent",
        analysis_type=message.analysis_type
    )
    
    messages_db[session_id].append(new_message)
    
    # Update file count if attachments are present
    if message.attachments:
        session = sessions_db[session_id]
        session.fileCount += len(message.attachments)
    
    # Generate assistant response using OpenAI
    asyncio.create_task(create_assistant_response(
        session_id, 
        message.content, 
        message.analysis_type, 
        message.attachments
    ))
    
    return new_message

async def create_assistant_response(session_id: str, user_message: str, analysis_type: str = None, attachments = None):
    """Create an assistant response after analyzing the request"""
    # First create a "thinking" message
    thinking_id = str(uuid.uuid4())
    thinking_message = Message(
        id=thinking_id,
        role="assistant",
        content="I'm analyzing your request...",
        timestamp=datetime.now(),
        status="sent",
        isStreaming=True,
        analysis_type=analysis_type
    )
    
    messages_db[session_id].append(thinking_message)
    
    # Check if there are files to analyze
    file_paths = []
    if attachments:
        print(f"Processing {len(attachments)} attachments")
        for attachment in attachments:
            file_id = attachment.id
            
            # Check if the file exists in the database
            if file_id in files_db:
                file_name = files_db[file_id].name
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
    previous_messages = messages_db[session_id][:-1]  # Exclude the thinking message we just added
    for msg in previous_messages[-10:]:
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
    for i, msg in enumerate(messages_db[session_id]):
        if msg.id == thinking_id:
            messages_db[session_id][i].content = response_content
            messages_db[session_id][i].isStreaming = False
            break
