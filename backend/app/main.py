from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="PCBuild Assist API",
    description="Smart PC component builder with Algolia integration for non-conversational proactive assistance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:5173", "http://localhost:3000"],  # Vite default + React default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes
from app.routes import components, compatibility, suggestions

# Include routers
app.include_router(components.router, prefix="/api/components", tags=["Components"])
app.include_router(compatibility.router, prefix="/api/compatibility", tags=["Compatibility"])
app.include_router(suggestions.router, prefix="/api/suggestions", tags=["Suggestions"])

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "PCBuild Assist API",
        "version": "1.0.0",
        "description": "Smart PC component builder with Algolia integration",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "PCBuild Assist API"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
