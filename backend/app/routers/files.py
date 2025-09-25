from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form, Depends
from typing import List
import uuid
import os
import shutil
from datetime import datetime
from sqlalchemy.orm import Session as SQLAlchemySession

from app.models.schemas import FileAttachment as FileAttachmentSchema
from app.models.database import FileAttachment as FileAttachmentModel
from app.utils.database import get_db

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=FileAttachmentSchema)
async def upload_file(file: UploadFile = File(...), db: SQLAlchemySession = Depends(get_db)):
    """Upload a file and return its metadata"""
    file_id = str(uuid.uuid4())
    
    # Save the file
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create file metadata
    file_attachment = FileAttachmentModel(
        id=file_id,
        name=file.filename,
        size=os.path.getsize(file_path),
        type=file.content_type or "application/octet-stream",
        uploadProgress=100,
        status="uploaded"
    )
    
    # Store in database
    db.add(file_attachment)
    db.commit()
    db.refresh(file_attachment)
    
    return file_attachment

@router.get("/{file_id}", response_model=FileAttachmentSchema)
async def get_file(file_id: str, db: SQLAlchemySession = Depends(get_db)):
    """Get file metadata by ID"""
    file_attachment = db.query(FileAttachmentModel).filter(FileAttachmentModel.id == file_id).first()
    if not file_attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File with ID {file_id} not found"
        )
    
    return file_attachment

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id: str, db: SQLAlchemySession = Depends(get_db)):
    """Delete a file"""
    file_attachment = db.query(FileAttachmentModel).filter(FileAttachmentModel.id == file_id).first()
    if not file_attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File with ID {file_id} not found"
        )
    
    # Find the file on disk
    file_name = file_attachment.name
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file_name}")
    
    # Delete from disk if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete from database
    db.delete(file_attachment)
    db.commit()
    
    return None
