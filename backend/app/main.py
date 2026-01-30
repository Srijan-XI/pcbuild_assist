from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os
import time

# Load environment variables
load_dotenv()

# Import core utilities
from app.core.logging import setup_logging, get_logger, generate_request_id, set_request_id, get_request_id
from app.core.rate_limit import limiter, rate_limit_exceeded_handler
from app.core.exceptions import APIException
from app.core.responses import error_response
from app.core.cache import cache

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting PCBuild Assist API", data={
        "version": "1.0.0",
        "environment": os.getenv("ENV", "development")
    })
    yield
    # Shutdown
    logger.info("Shutting down PCBuild Assist API")
    cache.clear()


# Create FastAPI app with enhanced configuration
app = FastAPI(
    title="PCBuild Assist API",
    description="""
## Smart PC Component Builder API

Powered by **Algolia** for intelligent, non-conversational assistance.

### Features
- 🔍 **Smart Search** - Fast, typo-tolerant component search
- ✅ **Compatibility Checking** - Validate CPU-motherboard, RAM type, PSU wattage
- 💡 **Intelligent Suggestions** - Multi-factor scoring for recommendations
- ⚡ **Performance** - Caching and rate limiting for reliability

### Authentication
Currently no authentication required. Rate limits apply per IP.

### Rate Limits
- Default: 100 requests/minute
- Search: 30 requests/minute
- Heavy operations: 10 requests/minute
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    responses={
        400: {"description": "Bad Request - Invalid parameters"},
        404: {"description": "Not Found - Resource doesn't exist"},
        422: {"description": "Validation Error - Invalid input data"},
        429: {"description": "Too Many Requests - Rate limit exceeded"},
        500: {"description": "Internal Server Error"},
        503: {"description": "Service Unavailable - External service down"}
    }
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(429, rate_limit_exceeded_handler)

# Configure CORS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
allowed_origins = [
    frontend_url,
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # React default
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

# Add production origins if configured
if os.getenv("PRODUCTION_ORIGIN"):
    allowed_origins.append(os.getenv("PRODUCTION_ORIGIN"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Processing-Time", "X-RateLimit-Remaining"],
)


# ==================== MIDDLEWARE ====================

@app.middleware("http")
async def request_middleware(request: Request, call_next):
    """
    Middleware for request tracking, timing, and logging.
    """
    # Generate and set request ID
    request_id = request.headers.get("X-Request-ID") or generate_request_id()
    set_request_id(request_id)
    
    # Record start time
    start_time = time.perf_counter()
    
    # Log request
    logger.info(f"{request.method} {request.url.path}", data={
        "method": request.method,
        "path": request.url.path,
        "query": str(request.query_params),
        "client_ip": request.client.host if request.client else "unknown"
    })
    
    try:
        # Process request
        response: Response = await call_next(request)
        
        # Calculate processing time
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        # Add custom headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Processing-Time"] = str(process_time)
        
        # Log response
        logger.info(f"Response {response.status_code}", data={
            "status_code": response.status_code,
            "processing_time_ms": process_time
        })
        
        return response
        
    except Exception as e:
        # Log error
        process_time = int((time.perf_counter() - start_time) * 1000)
        logger.error(f"Request failed: {str(e)}", data={
            "error": str(e),
            "processing_time_ms": process_time
        })
        raise


# ==================== EXCEPTION HANDLERS ====================

@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    """Handle custom API exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            code=exc.code,
            message=exc.message,
            details=exc.details,
            request_id=get_request_id()
        ),
        headers=exc.headers
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,
        content=error_response(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details={"errors": errors},
            request_id=get_request_id()
        )
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.exception(f"Unhandled exception: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content=error_response(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred",
            details={"type": type(exc).__name__} if os.getenv("ENV") != "production" else None,
            request_id=get_request_id()
        )
    )


# ==================== ROUTES ====================

# Import routes
from app.routes import components, compatibility, suggestions

# Include routers with tags
app.include_router(
    components.router,
    prefix="/api/components",
    tags=["Components"]
)
app.include_router(
    compatibility.router,
    prefix="/api/compatibility",
    tags=["Compatibility"]
)
app.include_router(
    suggestions.router,
    prefix="/api/suggestions",
    tags=["Suggestions"]
)


# ==================== ROOT ENDPOINTS ====================

@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint - API information and quick links.
    """
    return {
        "name": "PCBuild Assist API",
        "version": "1.0.0",
        "description": "Smart PC component builder with Algolia integration",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "health": "/health",
            "components": "/api/components",
            "compatibility": "/api/compatibility",
            "suggestions": "/api/suggestions"
        }
    }


@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint for monitoring.
    Returns service status and cache statistics.
    """
    return {
        "status": "healthy",
        "service": "PCBuild Assist API",
        "version": "1.0.0",
        "cache_stats": cache.stats()
    }


@app.get("/api/cache/stats", tags=["System"])
async def cache_stats():
    """
    Get cache statistics.
    Useful for monitoring cache performance.
    """
    return {
        "success": True,
        "data": cache.stats()
    }


@app.post("/api/cache/clear", tags=["System"])
async def clear_cache(cache_name: str = None):
    """
    Clear cache (admin endpoint).
    Optionally specify a specific cache to clear.
    """
    cache.clear(cache_name)
    return {
        "success": True,
        "message": f"Cache {'`' + cache_name + '`' if cache_name else 'all'} cleared"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)

