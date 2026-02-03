"""
Main FastAPI Application

This is the entry point for the FastAPI application.
It brings together:
- API routers (the endpoints)
- Configuration
- Database connection
- CORS middleware

KEY FASTAPI CONCEPTS:
---------------------
- APIRouter: A way to group related endpoints into separate files
- Middleware: Code that runs before every request (e.g., for CORS)
- Lifespan Events: Code that runs at startup and shutdown (e.g., to create DB tables)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.config import get_settings
from .core.database import engine
from .models import models
from .routers import samples, qc_metrics, pipeline_runs


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for application startup and shutdown.
    
    Startup: Creates all database tables if they don't exist.
    Shutdown: (No action needed here, but could be used for cleanup)
    """
    print("Starting up...")
    # This is NOT recommended for production with Alembic.
    # In production, you should manage migrations with Alembic.
    # For this portfolio project, it simplifies setup.
    models.Base.metadata.create_all(bind=engine)
    print("Database tables checked/created.")
    yield
    print("Shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title=get_settings().app_name,
    version=get_settings().app_version,
    lifespan=lifespan
)

# Add CORS middleware
# This allows the Streamlit dashboard (running on a different port)
# to make requests to this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
# This keeps the main file clean and organizes endpoints by resource.
app.include_router(samples.router, prefix=get_settings().api_prefix, tags=["Samples"])
app.include_router(qc_metrics.router, prefix=get_settings().api_prefix, tags=["QC Metrics"])
app.include_router(pipeline_runs.router, prefix=get_settings().api_prefix, tags=["Pipeline Runs"])


@app.get("/", tags=["Health Check"])
def read_root():
    """Root endpoint for health checks."""
    return {"status": "ok", "message": f"Welcome to {get_settings().app_name}"}
