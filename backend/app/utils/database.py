from datetime import datetime
import uuid
from typing import Dict, List

from app.models.schemas import Message, Session, FileAttachment

# In-memory database
sessions_db: Dict[str, Session] = {}
messages_db: Dict[str, List[Message]] = {}
files_db: Dict[str, FileAttachment] = {}

# Initialize with minimal data
def init_db():
    # Create initial assistant message
    initial_message = Message(
        id=str(uuid.uuid4()),
        role="assistant",
        content="Hello! I'm your Report Agent. Upload Excel files, CSV, PDF, or VB reports, and I'll provide comprehensive analysis, extract key insights, and suggest actionable next steps. How can I help you today?",
        timestamp=datetime.now(),
        status="sent"
    )
    
    # Create a default session with just the initial message
    default_session_id = "default"
    default_session = Session(
        id=default_session_id,
        title="New Analysis",
        timestamp=datetime.now(),
        fileCount=0
    )
    
    sessions_db[default_session_id] = default_session
    messages_db[default_session_id] = [initial_message]

# Initialize the database
init_db()
