from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from typing import List
import uuid
import os
import shutil
from datetime import datetime

from app.models.schemas import FileAttachment
from app.utils.database import files_db

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=FileAttachment)
async def upload_file(file: UploadFile = File(...)):
    """Upload a file and return its metadata"""
    file_id = str(uuid.uuid4())
    
    # Save the file
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create file metadata
    file_attachment = FileAttachment(
        id=file_id,
        name=file.filename,
        size=os.path.getsize(file_path),
        type=file.content_type or "application/octet-stream",
        uploadProgress=100,
        status="uploaded"
    )
    
    # Store in database
    files_db[file_id] = file_attachment
    
    return file_attachment

@router.get("/{file_id}", response_model=FileAttachment)
async def get_file(file_id: str):
    """Get file metadata by ID"""
    if file_id not in files_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File with ID {file_id} not found"
        )
    
    return files_db[file_id]

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id: str):
    """Delete a file"""
    if file_id not in files_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File with ID {file_id} not found"
        )
    
    # Find the file on disk
    file_name = files_db[file_id].name
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file_name}")
    
    # Delete from disk if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete from database
    del files_db[file_id]
    
    return None
