import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import vulnerabilities
import upload
import ai_assessment
from services import ai_service

# Create tables
Base.metadata.create_all(bind=engine)

# Configure OpenAI
ai_service.configure_openai()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(vulnerabilities.router, prefix="/vulnerabilities")
app.include_router(upload.router, prefix="/upload")
app.include_router(ai_assessment.router, prefix="/vulnerabilities")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)