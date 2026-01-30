"""
Standardized API response models for PCBuild Assist API.
Ensures consistent response format across all endpoints.
"""
from typing import TypeVar, Generic, Optional, List, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')


class MetaData(BaseModel):
    """Response metadata."""
    request_id: Optional[str] = Field(None, description="Unique request identifier")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    version: str = Field(default="1.0.0", description="API version")
    processing_time_ms: Optional[int] = Field(None, description="Server processing time in milliseconds")


class PaginationInfo(BaseModel):
    """Pagination metadata."""
    page: int = Field(0, ge=0, description="Current page (0-indexed)")
    per_page: int = Field(20, ge=1, le=100, description="Items per page")
    total_items: int = Field(0, ge=0, description="Total number of items")
    total_pages: int = Field(0, ge=0, description="Total number of pages")
    has_next: bool = Field(False, description="Whether there are more pages")
    has_prev: bool = Field(False, description="Whether there are previous pages")


class ErrorDetail(BaseModel):
    """Error response detail."""
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    field: Optional[str] = Field(None, description="Field that caused the error (for validation errors)")


class APIResponse(BaseModel, Generic[T]):
    """
    Standard API response wrapper.
    All API responses should use this format for consistency.
    """
    success: bool = Field(True, description="Whether the request was successful")
    data: Optional[T] = Field(None, description="Response data")
    error: Optional[ErrorDetail] = Field(None, description="Error details if success=False")
    meta: MetaData = Field(default_factory=MetaData, description="Response metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"id": "cpu_001", "name": "AMD Ryzen 9 9900X"},
                "error": None,
                "meta": {
                    "request_id": "abc-123",
                    "timestamp": "2025-01-30T12:00:00Z",
                    "version": "1.0.0",
                    "processing_time_ms": 42
                }
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Paginated API response wrapper.
    Used for list endpoints that support pagination.
    """
    success: bool = Field(True, description="Whether the request was successful")
    data: List[T] = Field(default_factory=list, description="List of items")
    pagination: PaginationInfo = Field(default_factory=PaginationInfo, description="Pagination info")
    error: Optional[ErrorDetail] = Field(None, description="Error details if success=False")
    meta: MetaData = Field(default_factory=MetaData, description="Response metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": [{"id": "cpu_001", "name": "AMD Ryzen 9 9900X"}],
                "pagination": {
                    "page": 0,
                    "per_page": 20,
                    "total_items": 100,
                    "total_pages": 5,
                    "has_next": True,
                    "has_prev": False
                },
                "error": None,
                "meta": {
                    "request_id": "abc-123",
                    "timestamp": "2025-01-30T12:00:00Z",
                    "version": "1.0.0"
                }
            }
        }


class SearchResponse(PaginatedResponse[T], Generic[T]):
    """
    Search response with additional search metadata.
    """
    query: str = Field("", description="Search query")
    filters_applied: Dict[str, Any] = Field(default_factory=dict, description="Applied filters")
    facets: Optional[Dict[str, Any]] = Field(None, description="Available facets/filters")


# Helper functions for creating responses

def success_response(
    data: Any,
    request_id: Optional[str] = None,
    processing_time_ms: Optional[int] = None
) -> dict:
    """Create a success response dict."""
    return {
        "success": True,
        "data": data,
        "error": None,
        "meta": {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
            "processing_time_ms": processing_time_ms
        }
    }


def error_response(
    code: str,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None
) -> dict:
    """Create an error response dict."""
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "details": details
        },
        "meta": {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0"
        }
    }


def paginated_response(
    data: List[Any],
    page: int,
    per_page: int,
    total_items: int,
    request_id: Optional[str] = None,
    processing_time_ms: Optional[int] = None,
    query: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None
) -> dict:
    """Create a paginated response dict."""
    total_pages = (total_items + per_page - 1) // per_page if per_page > 0 else 0
    
    response = {
        "success": True,
        "data": data,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages - 1,
            "has_prev": page > 0
        },
        "error": None,
        "meta": {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
            "processing_time_ms": processing_time_ms
        }
    }
    
    if query is not None:
        response["query"] = query
    if filters is not None:
        response["filters_applied"] = filters
    
    return response
