"""
Main FastAPI application with authentication routes and CORS configuration.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth_router

# Create FastAPI application instance
app = FastAPI(
    title="Transflow Backend API",
    description="RESTful Authentication API with FastAPI and Appwrite integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router)


@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - health check.
    
    Returns:
        dict: API status and version information
    """
    return {
        "status": "ok",
        "message": "Transflow Backend API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy"}
