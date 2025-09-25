# Report Agent Backend

This is the backend for the Report Agent application, which uses FastAPI and OpenAI to analyze business documents.

## Features

- File upload and processing (Excel, CSV, PDF, VB reports)
- OpenAI integration for document analysis
- Different analysis types (summarize, trends, KPIs, actions, compare)
- Session management for saving and retrieving previous analyses

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure OpenAI API key:
   - Rename `.env.example` to `.env` or edit the existing `.env` file
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     OPENAI_MODEL=gpt-4o
     ```
   - **Important**: If you don't have an OpenAI API key, the application will still work but will use simulated responses instead of real AI analysis.
   - You can use different OpenAI models by changing the `OPENAI_MODEL` value. For example:
     ```
     OPENAI_MODEL=gpt-4o
     OPENAI_MODEL=gpt-4.1-mini
     OPENAI_MODEL=gpt-3.5-turbo
     ```

3. Run the server:
   ```
   python run.py
   ```

4. Run the frontend:
   ```
   npm run dev
   ```

5. Or use the start.bat script to run both:
   ```
   .\start.bat
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
- `POST /api/messages/{session_id}` - Create a new message in a session with optional analysis type

### Files

- `POST /api/files/upload` - Upload a file
- `GET /api/files/{file_id}` - Get file metadata
- `DELETE /api/files/{file_id}` - Delete a file

## Analysis Types

The backend supports different types of analysis:

1. **Summarize** - Provides a comprehensive summary of the uploaded documents
2. **Trends** - Analyzes and identifies key trends in the data
3. **KPIs** - Extracts and highlights key performance indicators
4. **Actions** - Generates actionable recommendations based on the analysis
5. **Compare** - Compares information across multiple documents

To specify an analysis type, include the `analysis_type` field in the message creation request:

```json
{
  "content": "Please analyze these files",
  "role": "user",
  "attachments": [...],
  "analysis_type": "summarize"
}
```

## File Processing

The backend can process various file types:

- **Excel** (.xlsx, .xls) - Extracts data from all sheets
- **CSV** (.csv) - Parses and formats the data
- **PDF** (.pdf) - Extracts text content with support for non-English characters
- **Text** (.txt, etc.) - Reads the raw text

Files are stored in the `uploads` directory with a UUID prefix to avoid name collisions.

## Troubleshooting

If you encounter issues with the OpenAI integration:

1. **API Key Issues**: Make sure your OpenAI API key is valid and correctly set in the `.env` file.
2. **Model Availability**: Ensure the model specified in `OPENAI_MODEL` is available for your OpenAI account.
   - The application will automatically try fallback models if the specified model is not available
   - Fallback models include: gpt-4o, gpt-3.5-turbo, gpt-4
3. **PDF Processing**: If PDF files aren't being analyzed correctly:
   - Check if the PDF contains extractable text (not just images)
   - For PDFs with non-English characters, ensure they're properly encoded
   - Very large PDFs may exceed token limits; try with smaller files
4. **File Upload Issues**: If files aren't being processed correctly:
   - Make sure the file is properly uploaded to the backend
   - Check the console logs for any errors during file upload
   - Verify that the file format is supported (.pdf, .xlsx, .xls, .csv)
5. **Error Messages**: The application provides detailed error messages to help diagnose issues with the OpenAI API.

## How to Use

1. **Upload Files**:
   - Click the "Upload" button to show the upload zone
   - Select one or more files (.pdf, .xlsx, .xls, .csv)
   - Wait for the files to upload

2. **Ask Questions**:
   - Type your question about the uploaded files
   - Click "Send" to submit your question
   - The AI will analyze the files and provide a response

3. **Use Analysis Types**:
   - Click on one of the analysis buttons (Summarize, Analyze Trends, Extract KPIs, Action Items, Compare)
   - Each button will trigger a different type of analysis on the uploaded files
   - The AI will use the appropriate prompt template for the selected analysis type
