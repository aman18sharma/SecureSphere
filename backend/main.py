"""Main entry point for the FastAPI vulnerability assessment application."""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
import vulnerabilities
import upload
import ai_assessment

# Initialize and configure the application
def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI app instance.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="AI-Driven Vulnerability Assessment API")

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict this to specific domains
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routers
    app.include_router(vulnerabilities.router, prefix="/vulnerabilities", tags=["Vulnerabilities"])
    app.include_router(upload.router, prefix="/upload", tags=["Upload"])
    app.include_router(ai_assessment.router, prefix="/vulnerabilities", tags=["AI Assessment"])

    return app


app = create_app()

# Entry point for running with `python main.py`
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
