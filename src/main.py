"""
ISHelper Email API - Main Application Module

This module initializes the FastAPI application with all routes and configuration.
It handles application startup and shutdown events, and configures the API metadata.

Author: ISHelper Team
Version: 1.0.0
"""

from dotenv import load_dotenv
from fastapi import FastAPI
from config.settings import settings
from routes import mail_router
from utils.logger import get_logger


logger = get_logger(__name__)

app = FastAPI(
    title="ISHelper Email API",
    description="API for sending contact emails through the ISHelper platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include mail router with all mail-related endpoints
app.include_router(mail_router)


@app.on_event("startup")
async def startup_event():
    """Handle application startup events.
    
    Logs application startup information.
    """
    logger.info(f"Starting API")


@app.on_event("shutdown")
async def shutdown_event():
    """Handle application shutdown events.
    
    Logs application shutdown information.
    """
    logger.info(f"Stopping API")

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Uvicorn server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.api_port
    )
