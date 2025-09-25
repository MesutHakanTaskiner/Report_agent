# Report Agent Chat Application

This is a full-stack application for analyzing business reports and documents. It consists of a React TypeScript frontend and a Python FastAPI backend.

## Features

- Upload and analyze business documents (Excel, CSV, PDF, VB reports)
- Chat interface for interacting with the report analysis agent
- Session management for saving and retrieving previous analyses
- Comprehensive analysis including summaries, KPIs, trends, and actionable insights

## Project Structure

- `src/` - Frontend React TypeScript code
- `backend/` - Python FastAPI backend code
  - `app/` - Main application code
    - `routers/` - API route handlers
    - `models/` - Data models and schemas
    - `services/` - Business logic
    - `utils/` - Utility functions

## Getting Started

### Prerequisites

- Node.js (v16+)
- Python (v3.8+)
- npm or yarn

### Installation

1. Clone the repository
2. Install frontend dependencies:
   ```
   npm install
   ```
3. Install backend dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

### Running the Application

You can run both the frontend and backend with a single command:

```
start.bat
```

Or run them separately:

**Backend:**
```
cd backend
python run.py
```

**Frontend:**
```
npm run dev
```

## API Endpoints

### Sessions

- `GET /api/sessions` - Get all sessions
- `GET /api/sessions/{session_id}` - Get a specific session
- `POST /api/sessions` - Create a new session
- `PUT /api/sessions/{session_id}` - Update a session
- `DELETE /api/sessions/{session_id}` - Delete a session
- `PUT /api/sessions/{session_id}/favorite` - Toggle favorite status

### Messages

- `GET /api/messages/{session_id}` - Get all messages for a session
- `POST /api/messages/{session_id}` - Create a new message in a session

### Files

- `POST /api/files/upload` - Upload a file
- `GET /api/files/{file_id}` - Get file metadata
- `DELETE /api/files/{file_id}` - Delete a file

## Technologies Used

### Frontend
- React
- TypeScript
- Ant Design
- Axios

### Backend
- Python
- FastAPI
- Uvicorn
