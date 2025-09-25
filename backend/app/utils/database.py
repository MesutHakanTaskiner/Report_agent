from datetime import datetime
import uuid
from typing import Dict, List

from app.models.schemas import Message, Session, FileAttachment

# In-memory database
sessions_db: Dict[str, Session] = {}
messages_db: Dict[str, List[Message]] = {}
files_db: Dict[str, FileAttachment] = {}

# Initialize with empty data structures
def init_db():
    # Create a default session with no messages
    default_session_id = "default"
    default_session = Session(
        id=default_session_id,
        title="New Analysis",
        timestamp=datetime.now(),
        fileCount=0
    )
    
    sessions_db[default_session_id] = default_session
    messages_db[default_session_id] = []  # Empty messages list

# Initialize the database
init_db()
