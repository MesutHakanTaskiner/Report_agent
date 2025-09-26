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

## Identified Shortcomings

### Documentation
- Missing detailed API documentation with request/response examples
- No troubleshooting guide or common issues section
- No explanation of the analysis types (summarize, trends, kpis, actions, compare)
- Missing information about file size limits and supported formats
- No deployment instructions for production environments
- No information about potential dependency conflicts and their resolution

### Known Issues
- There may be compatibility issues between numpy and pandas versions, resulting in errors like:
  ```
  ValueError: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject
  ```
  This can be resolved by reinstalling these packages in the correct order:
  ```
  pip uninstall -y numpy pandas
  pip install numpy==1.24.3
  pip install pandas==2.1.1
  ```

### Environment Setup
- No clear instructions for setting up the OpenAI API key
- Missing database configuration options (currently defaults to SQLite)
- No information about required Python and Node.js versions
- No Docker configuration for containerized deployment
- Missing CORS configuration for production environments

### Code Structure
- Error handling could be improved with more specific error messages
- No logging configuration for production environments
- No unit or integration tests
- No database migration scripts for schema changes
- No authentication/authorization mechanism for API endpoints

## Getting Started

### Prerequisites

- Node.js (v16+)
- Python (v3.11.0)
- npm or yarn

### Running the Application

Simply run the start.bat script from the root directory of the project:

```
start.bat
```

The start.bat script will:
1. Check if Node.js dependencies exist and install them if needed
2. Check if a Python virtual environment exists in the backend folder
3. Create one if it doesn't exist
4. Activate the virtual environment
5. Install the required Python dependencies
6. Start the backend server in the virtual environment
7. Start the frontend development server

No manual installation steps are required - everything is handled by the start.bat script.

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

## Environment Details

### Backend Environment
- The application uses OpenAI API for generating responses
- Requires an OpenAI API key to be set in the `.env` file (copy from `.env.example`)
- Default model is set to `gpt-4.1-mini` with fallbacks to other models if unavailable
- Uses SQLite as the default database (stored in `report_agent.db`)
- File uploads are stored in a local `uploads` directory
- Supports analysis of Excel, CSV, PDF, and text files
- Python virtual environment (venv) is recommended but not enforced
- No requirements pinning or dependency management beyond basic requirements.txt
- No environment-specific configuration for development vs. production

### Frontend Environment
- Built with React 19 and TypeScript
- Uses Ant Design for UI components
- Communicates with backend via Axios HTTP client
- Runs on Vite development server
- Configured for modern browsers with ESLint for code quality
