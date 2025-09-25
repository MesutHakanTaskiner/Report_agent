from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

# Association table for message-attachment relationship
message_attachment = Table(
    'message_attachment',
    Base.metadata,
    Column('message_id', String, ForeignKey('messages.id')),
    Column('attachment_id', String, ForeignKey('file_attachments.id'))
)

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    fileCount = Column(Integer, default=0)
    isFavorite = Column(Boolean, default=False)
    
    # Relationship with messages
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    
    @classmethod
    def create_new(cls, title):
        """Helper method to create a new session with a UUID"""
        return cls(
            id=str(uuid.uuid4()),
            title=title,
            timestamp=datetime.now(),
            fileCount=0,
            isFavorite=False
        )

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, index=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    status = Column(String, default="sent")
    isStreaming = Column(Boolean, nullable=True)
    analysis_type = Column(String, nullable=True)
    
    # Foreign key to session
    session_id = Column(String, ForeignKey("sessions.id"))
    
    # Relationships
    session = relationship("Session", back_populates="messages")
    attachments = relationship(
        "FileAttachment", 
        secondary=message_attachment,
        back_populates="messages"
    )
    
    @classmethod
    def create_new(cls, role, content, session_id, analysis_type=None):
        """Helper method to create a new message with a UUID"""
        return cls(
            id=str(uuid.uuid4()),
            role=role,
            content=content,
            timestamp=datetime.now(),
            session_id=session_id,
            status="sent",
            analysis_type=analysis_type
        )

class FileAttachment(Base):
    __tablename__ = "file_attachments"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    uploadProgress = Column(Integer, default=100)
    status = Column(String, default="uploaded")
    
    # Relationship with messages
    messages = relationship(
        "Message", 
        secondary=message_attachment,
        back_populates="attachments"
    )
