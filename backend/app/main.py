"""Main application entry point"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analysis import router as analysis_router
from app.api.prompt_edit import router as prompt_edit_router
from app.config import settings
from app.database import Base, engine

# Import models to ensure they are registered with SQLAlchemy
import app.models.analysis  # noqa: F401
import app.models.prompt_edit  # noqa: F401

# Create tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis_router)
app.include_router(prompt_edit_router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI Backend",
        "docs": "/docs",
        "redoc": "/redoc",
    }


# Example API routes
@app.get("/api/items")
async def list_items():
    """List all items"""
    return {"items": []}


@app.post("/api/items")
async def create_item(name: str, description: str = ""):
    """Create a new item"""
    return {"id": 1, "name": name, "description": description}


@app.get("/api/items/{item_id}")
async def get_item(item_id: int):
    """Get item by ID"""
    return {"id": item_id, "name": "Sample Item"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug,
    )
