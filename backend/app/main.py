from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routers import sessions, messages, files

app = FastAPI(
    title="Report Agent API",
    description="Backend API for the Report Agent Chat application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])
app.include_router(files.router, prefix="/api/files", tags=["Files"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Report Agent API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
