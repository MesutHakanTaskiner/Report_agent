from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class FileAttachment(BaseModel):
    id: str
    name: str
    size: int
    type: str
    uploadProgress: int = 100
    status: str = "uploaded"

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    role: str = "user"
    attachments: Optional[List[FileAttachment]] = None
    analysis_type: Optional[str] = "summarize"  # New field for analysis type

class Message(MessageBase):
    id: str
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    attachments: Optional[List[FileAttachment]] = None
    status: str = "sent"
    isStreaming: Optional[bool] = None
    analysis_type: Optional[str] = None  # Store the analysis type used

    class Config:
        from_attributes = True

class SessionBase(BaseModel):
    title: str

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: str
    title: str
    timestamp: datetime = Field(default_factory=datetime.now)
    fileCount: int = 0
    isFavorite: Optional[bool] = False
    messages: Optional[List[Message]] = None

    class Config:
        from_attributes = True

class AnalysisRequest(BaseModel):
    file_ids: List[str]
    analysis_type: str = "summarize"
    user_message: Optional[str] = None
