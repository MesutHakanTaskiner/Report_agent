from datetime import datetime
import uuid
from typing import Dict, List

from app.models.schemas import Message, Session, FileAttachment

# In-memory database
sessions_db: Dict[str, Session] = {}
messages_db: Dict[str, List[Message]] = {}
files_db: Dict[str, FileAttachment] = {}

# Initialize with some sample data
def init_db():
    # Create initial assistant message
    initial_message = Message(
        id=str(uuid.uuid4()),
        role="assistant",
        content="Hello! I'm your Report Agent. Upload Excel files, CSV, PDF, or VB reports, and I'll provide comprehensive analysis, extract key insights, and suggest actionable next steps. How can I help you today?",
        timestamp=datetime.now(),
        status="sent"
    )
    
    # Sample sessions
    session1_id = str(uuid.uuid4())
    session1 = Session(
        id=session1_id,
        title="Q3 Sales Analysis",
        timestamp=datetime.now(),
        fileCount=3,
        isFavorite=True
    )
    
    session2_id = str(uuid.uuid4())
    session2 = Session(
        id=session2_id,
        title="Marketing Report Review",
        timestamp=datetime.now(),
        fileCount=2
    )
    
    session3_id = str(uuid.uuid4())
    session3 = Session(
        id=session3_id,
        title="Financial Dashboard",
        timestamp=datetime.now(),
        fileCount=5
    )
    
    # Add sessions to database
    sessions_db[session1_id] = session1
    sessions_db[session2_id] = session2
    sessions_db[session3_id] = session3
    
    # Add messages for each session
    messages_db[session1_id] = [
        Message(
            id=str(uuid.uuid4()),
            role="assistant",
            content="I've analyzed your Q3 sales reports. Here are the key findings:",
            timestamp=datetime.now(),
            status="sent"
        ),
        Message(
            id=str(uuid.uuid4()),
            role="user",
            content="What are the main trends in revenue?",
            timestamp=datetime.now(),
            status="sent"
        ),
        Message(
            id=str(uuid.uuid4()),
            role="assistant",
            content="Revenue increased by 23% compared to Q2, with strongest growth in the enterprise segment (+45%). Digital products showed exceptional performance.",
            timestamp=datetime.now(),
            status="sent"
        )
    ]
    
    messages_db[session2_id] = [
        Message(
            id=str(uuid.uuid4()),
            role="assistant",
            content="Marketing report analysis complete. Campaign performance shows mixed results.",
            timestamp=datetime.now(),
            status="sent"
        ),
        Message(
            id=str(uuid.uuid4()),
            role="user",
            content="Which campaigns performed best?",
            timestamp=datetime.now(),
            status="sent"
        ),
        Message(
            id=str(uuid.uuid4()),
            role="assistant",
            content="Social media campaigns had 3x ROI, while email marketing achieved 45% open rates. Paid search needs optimization.",
            timestamp=datetime.now(),
            status="sent"
        )
    ]
    
    messages_db[session3_id] = [
        Message(
            id=str(uuid.uuid4()),
            role="assistant",
            content="Financial dashboard loaded. All KPIs are within expected ranges.",
            timestamp=datetime.now(),
            status="sent"
        ),
        Message(
            id=str(uuid.uuid4()),
            role="user",
            content="Show me the cash flow analysis",
            timestamp=datetime.now(),
            status="sent"
        ),
        Message(
            id=str(uuid.uuid4()),
            role="assistant",
            content="Cash flow remains positive with $2.3M in operating activities. Working capital improved by 15%.",
            timestamp=datetime.now(),
            status="sent"
        )
    ]
    
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
